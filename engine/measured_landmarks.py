import pyglet, resources

class Measured_Landmark(pyglet.sprite.Sprite):
	def __init__(self, *args, **kwargs):
		super(Measured_Landmark, self).__init__(img = resources.measured_landmark_image, *args,**kwargs)


	def update(self, x, y):
		self.x = x
		self.y = y
		
	
