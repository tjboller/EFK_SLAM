import pyglet, resources

class Measured_Landmark(pyglet.sprite.Sprite):
	def __init__(self, *args, **kwargs):
		super(Measured_Landmark, self).__init__(img = resources.measured_landmark_image, *args,**kwargs)

	def update(self, x_measured, y_measured, x_robot, y_robot):
		
		#updates the position of the landmarks to the 
		self.x = x_robot + x_measured
		self.y = y_robot + y_measured
		
	
