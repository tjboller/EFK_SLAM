import pyglet, math, random

def distance(point_1=(0, 0), point_2=(0, 0)):
    """Returns the distance between two points"""
    return math.sqrt((point_1[0]-point_2[0])**2+(point_1[1]-point_2[1])**2)

def scan(landmarks):
	"""Finds the position of the landmarks with respect to the robots reference frame""" 

	scan = []
	for landmark in landmarks:

		error_x = random.gauss(0,5)
		error_y = random.gauss(0,5)

		x_distance = landmark.x + error_x
		y_distance = landmark.y + error_y

		
		scan.append((x_distance,y_distance))

	return scan


