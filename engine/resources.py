import pyglet

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

# Tell pyglet where to find the resources
pyglet.resource.path = ['../resources']
pyglet.resource.reindex()

# Load the main resources and get them to draw centered
real_robot_image = pyglet.resource.image("realrobot.png")
center_image(real_robot_image)

perfect_robot_image = pyglet.resource.image("ghostrobot.png")
center_image(perfect_robot_image)

landmark_image = pyglet.resource.image("landmark.png")
center_image(landmark_image)

measured_landmark_image = pyglet.resource.image('greendot.png')
center_image(measured_landmark_image)