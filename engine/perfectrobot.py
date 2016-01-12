import math
import resources
import realrobot
import pyglet
import random
import numpy as np
import ekf, realrobot
from pyglet.window import key


#same as real robot class but with no error in movements
class Perfect_Robot(pyglet.sprite.Sprite):
	def __init__(self, *args, **kwargs):
		super(Perfect_Robot, self).__init__(img = resources.perfect_robot_image, *args,**kwargs)

		# Set velocity and rotational speed of robot
		self.velocity = 200
		self.rotate_speed = 100.0

		#stores position history for later analysis
		self.position_history = [(self.x,self.y,self.rotation)]
		self.scan_history = []

		# Size of state is 3 + 2 * num of landmarks 
		num_landmarks = 30
		size = 3 + 2 * num_landmarks

		# Initialize EKF Vectors
		self.cov = np.zeros((size,size))
		self.G  = np.eye(size)
		self.V = np.zeros((size,2))
		self.state_error = np.array([[.5**2,0],[0,1**2]])
		self.obs_error = np.array([[5**2,0],[0,5**2]])

		self.state = np.zeros((size,1))
		self.update_num = 0
		#Keyboard events
		self.key_handler = key.KeyStateHandler()


	def update(self, dt, landmarks,scans,real_robot, EKF):

		delta_x= 0
		delta_y = 0
		delta_theta =0


		################################## Prediction ###############################

		# Input Controls
		if self.key_handler[key.LEFT]:
			delta_theta = -self.rotate_speed * dt
			self.rotation += delta_theta

		if self.key_handler[key.RIGHT]:
			delta_theta = self.rotate_speed * dt
			self.rotation += delta_theta

		if self.key_handler[key.UP]:
			delta_x = self.velocity * math.cos(math.radians(self.rotation%360)) * dt
			delta_y = self.velocity * -math.sin(math.radians(self.rotation%360)) * dt
			self.x += delta_x
			#rotation is defined as clockwise, hence the negative
			self.y += delta_y



		if EKF:
			# Build G
			self.G[0][2] = -delta_y
			self.G[1][2] = delta_x

			# Build V
			self.V[0][0] = delta_x
			self.V[1][0] = delta_y
			self.V[2][1] = delta_theta

			# Compute Prediction Covarience
			self.cov = np.dot(np.dot(self.G,self.cov),np.transpose(self.G))+ np.dot(np.dot(self.V,self.state_error),self.V.T)

			# Build State
			self.state[0] = self.x
			self.state[1] = self.y
			self.state[2] = self.rotation
			self.update_num += 1

			# Add new 
			if self.state[3+ 2*len(scans) -1] ==0:
				for i in range(3,2*len(scans)):
					self.cov[i][i] = 10**5


				count = 3
				for scan in scans:
					self.state[count] = scan[0]
					self.state[count+1] = scan[1]
					count += 2
				



			##############################     Correction     #######################################





			# Find measurements to landmarks for the prediction model and real robot
			count = 3
			for scan in scans:


				# Find the innovation 
				r_measured = math.sqrt((scan[0] - real_robot.x)**2+(scan[1] - real_robot.y)**2 )
				alpha_measured = (math.degrees(math.atan2(scan[1] - real_robot.y,scan[0] - real_robot.x)) + real_robot.rotation)%360


				r_expect = math.sqrt((scan[0] - self.x)**2+(scan[1] - self.y)**2 )
				alpha_expect = float((math.degrees(math.atan2(scan[1] - self.y,scan[0] - self.x)) + self.rotation))%360

				# for substracting angles if the difference is larger than 180, take 360 - ans
				if (alpha_measured - alpha_expect) > 180:
					angle_error = 360-(alpha_measured - alpha_expect)
				else:
					angle_error = -(alpha_measured - alpha_expect)

				# Define innovation
				self.innovation = np.zeros((2,1))
				self.innovation[0] = r_measured - r_expect
				self.innovation[1] = angle_error


				# Build H matrix
				self.H = np.zeros((2, 3+2*len(scans)))

				self.H2 = np.array(
					[[-(scan[0] - real_robot.x)/r_measured,-(scan[1] - real_robot.y)/r_measured],
					[(scan[1] - real_robot.y)/r_measured**2,-(scan[0] - real_robot.x)/r_measured**2]])


				self.H[:,:2] = self.H2
				self.H[0][2] = 0
				self.H[1][2] = -1
				self.H[:,count:count+2] = - self.H2
				self.state[count] = (1-(1./self.update_num))*self.state[count] + (1./self.update_num)*scan[0]
				self.state[count+1] = (1-(1./self.update_num))*self.state[count+1] + (1./self.update_num)*scan[1]
				count = count + 2

				# Build Kalman Gain
				kal_const = np.linalg.inv(np.dot(np.dot(self.H,self.cov),self.H.T) + self.obs_error)
				self.K = np.dot(np.dot(self.cov,self.H.T), kal_const)


				# Update Variance
				var_const = np.eye(3+2*len(scans))
				self.cov = np.dot((var_const -np.dot(self.K,self.H)),self.cov)

				# Correct State
				self.state = self.state + np.dot(self.K,self.innovation)


				self.x = self.state[0]
				self.y = self.state[1]
				self.rotation = self.state[2]








