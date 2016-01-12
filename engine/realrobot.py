import math
import resources, util, landmark
import pyglet
import random
from pyglet.window import key

class Real_Robot(pyglet.sprite.Sprite):
	rotation_var = .5
	forward_var = .2
	def __init__(self, *args, **kwargs):
		super(Real_Robot, self).__init__(img = resources.real_robot_image, *args,**kwargs)

		# Set velocity and rotational speed of robot
		self.velocity = 200
		self.rotate_speed = 100.0

		# Stores position history and distance to landmarks for analysis 
		self.position_history = [(self.x,self.y,self.rotation)]
		self.distance_history = []
		
		# Allows for keyboard events
		self.key_handler = key.KeyStateHandler()


	def update(self, dt):

		# Set movement error
		self.rotation_error = random.gauss(0,self.rotation_var)
		self.forward_error = random.gauss(0,self.forward_var)

		#Updates location/heading of robot with error
		if self.key_handler[key.LEFT]:
			self.rotation -= self.rotate_speed * dt * (1+ self.rotation_error)
		if self.key_handler[key.RIGHT]:
			self.rotation += self.rotate_speed * dt  * (1+ self.rotation_error)
		if self.key_handler[key.UP]:
			self.x += self.velocity * math.cos(math.radians(self.rotation%360)) * dt * (1+self.forward_error)
			# Rotation is defined as clockwise, hence the negative sine, (cosine is an even function so it doesnt matter)
			self.y += self.velocity * -math.sin(math.radians(self.rotation%360)) * dt *(1+self.forward_error)

		# Append position history
		#self.position_history.append((self.x,self.y,self.rotation))

	
