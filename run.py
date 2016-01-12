import pyglet, random
import numpy as np
import matplotlib.pyplot as plt
from engine import resources,realrobot, perfectrobot, landmark, util,ekf


# Global variable to keep track of what update number we are on (dont want to scan every update)
update_number = 0

# Set up a window
sim_window = pyglet.window.Window(1010, 600)

# Set up the batch
main_batch = pyglet.graphics.Batch()
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

# Initialize the perfect model robot, scale the image down
perfect_robot = perfectrobot.Perfect_Robot(x=400, y=300, batch = main_batch)
perfect_robot.scale = .75

# Initialize the real robot, scale the image down
real_robot = realrobot.Real_Robot(x=400, y=300, batch = main_batch)
real_robot.scale = .75

# Pick which landmark set up you want, grid numer of landmarks must be a perfect square
measured_landmarks, landmarks = landmark.random_landmarks(30, main_batch, [foreground,background])
#measured_landmarks,landmarks = landmark.grid_landmarks(16, main_batch,[foreground,background])

# Tells window that the robots respond to events
sim_window.push_handlers(real_robot.key_handler)
sim_window.push_handlers(perfect_robot.key_handler)

def update(dt):


	# EKF SWITCH
	EKF = False


	# Count the Update 
	global update_number
	update_number += 1

	real_robot.update(dt)

	# Measure from real robot to landmarks
	scans = util.scan(landmarks)

	perfect_robot.update(dt,landmarks,scans,real_robot,EKF)
	
	# Scan every 20th update
	if update_number%10 == 0:

		#Update the GUI 
		count = 3
		for i in range(len(measured_landmarks)):
			scan_x,scan_y  = scans[i]


			# Update where the measured landmarks are with respect to the model robot
			if not EKF:
				# Print the measured locations
				measured_landmarks[i].update(scan_x-real_robot.x,scan_y-real_robot.y,perfect_robot.x, perfect_robot.y)
			
			if EKF:
				measured_landmarks[i].x = perfect_robot.state[count]
				measured_landmarks[i].y = perfect_robot.state[count+1]
			count += 2


# Draw the window
@sim_window.event
def on_draw():
    sim_window.clear()
    main_batch.draw()

if __name__ == "__main__":
	#update the simulation 120 times a second
	pyglet.clock.schedule_interval(update, 1/120.0)

    # Tell pyglet to do its thing
	pyglet.app.run()
