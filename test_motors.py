# This file is created to test inputing different power level to each motor
# Last updated: 8/28/24

from robot_hat import Motors
import time

motors = Motors()  # create motors object from class Motors

# identify each motor
LEFT = 1  
RIGHT = 2

# Left and right motors have opposite speed to go in the same direction

# go forward
motors[LEFT].speed(-50)
motors[RIGHT].speed(50)
time.sleep(0.5)
motors.stop()
time.sleep(1)

# reverse
motors[LEFT].speed(50)
motors[RIGHT].speed(-50)
time.sleep(0.5)
motors.stop()

# turn left 
motors[LEFT].speed(50)
motors[RIGHT].speed(50)
time.sleep(0.5)
motors.stop()

# turn right

