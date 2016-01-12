import pyglet, resources, random, util, math, update_landmarks



#randomly places landmarks
def random_landmarks(num_landmarks, batch = None, group = None):

	# Constants
	allowed_distance = 100
	landmarks = []
	measured_landmarks = []
	real_scale = .04
	measured_scale = .02


	while len(landmarks)<num_landmarks:

		# Initialize decision boolean
		too_close = False

		# Pick random point where landmark wont go off the screen
		rand_x = random.uniform(40,970)
		rand_y = random.uniform(40,560)

		# Create landmark and copy position for measured landmarks
		new_landmark = pyglet.sprite.Sprite(img = resources.landmark_image, x =rand_x, y = rand_y, batch = batch, group=group[1])
		new_measured_landmark = update_landmarks.Measured_Landmark(x = rand_y, y = rand_y ,batch = batch, group = group[0])
		
		#if first landmark append it to accepted lists
		if len(landmarks)==0:
			new_landmark.scale = real_scale
			new_measured_landmark.scale = measured_scale 
			landmarks.append(new_landmark)
			measured_landmarks.append(new_measured_landmark)

		# Check through list of established landmarks and make sure new one isnt too close
		else:
			for landmark in landmarks:
				if util.distance((new_landmark.x,new_landmark.y),(landmark.x,landmark.y)) < allowed_distance:
					too_close = True
					break

			if not too_close:
				new_measured_landmark.scale = measured_scale 
				new_landmark.scale = real_scale
				landmarks.append(new_landmark)
				measured_landmarks.append(new_measured_landmark)

	return (measured_landmarks, landmarks)

#spaces out landmarks equally
def grid_landmarks(num_landmarks, batch = None, group = None):
	"""Initializes landmarks in a grid, number must be a perfect square"""

	# Constants
	real_scale = .04
	measured_scale = .02
	landmarks = []
	measured_landmarks = []
	per_row = int(math.sqrt(num_landmarks))


	for row in range(per_row):
		for column in range(per_row):

			#draw a picture and see why this is right, dunno what else to say
			x_val =  (1010/(per_row+1))*(column+1)
			y_val = (600.0/(per_row+1))*(row+1)

			# Initializes the measured landmarks
			new_measured_landmark = update_landmarks.Measured_Landmark(x = x_val, y = y_val ,batch = batch, group = group[0])
			new_measured_landmark.scale = measured_scale

			# Initializes landmarks
			new_landmark = pyglet.sprite.Sprite(img = resources.landmark_image, x = x_val, y = y_val ,batch = batch, group = group[1])
			new_landmark.scale = real_scale

			# Creates the list of real and measured landmarks
			measured_landmarks.append(new_measured_landmark)
			landmarks.append(new_landmark)
			

	return (measured_landmarks,landmarks)

