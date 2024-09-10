# This file is created to test inputing different power level to each motor
# Last updated: 8/28/24

from picarx import Picarx
from robot_hat import Motors
import time
import math

path = []
power = 30
turningTime = 0.7     # for 90 degrees

motors = Motors()  # create motors object from class Motors

# identify each motor
LEFT = 1  
RIGHT = 2

# Left and right motors have opposite speed to go in the same direction

# go forward
#motors[LEFT].speed(-50)
#motors[RIGHT].speed(50)
#time.sleep(0.5)
#motors.stop()
#time.sleep(1)

# reverse
#motors[LEFT].speed(50)
#motors[RIGHT].speed(-50)
#time.sleep(0.5)
#motors.stop()

# turn left 
def PivotLeft():
    global motors
    motors[LEFT].speed(70)
    motors[RIGHT].speed(70)
    time.sleep(1.6)     # turn 90 degrees
    motors.stop()

# turn right
def PivotRight():
    global motors
    motors[LEFT].speed(-70)
    motors[RIGHT].speed(-70)
    time.sleep(1.6)
    motors.stop()

# This function returns the target destination 
# Returns a list of x,y
def get_final_coord():  
    endx = int(input("Enter destination x coordinate: "))
    endy = int(input("Enter destination y coordinate: "))
    end = [endx,endy]
    return end
    
# This function returns the starting position 
# Returns a list of x,y
def get_initial_coord():
    startx = int(input("Enter starting x coordinate: "))
    starty = int(input("Enter starting y coordinate: "))
    start = [startx,starty]
    return start

# This function returns error value in respect with the goal coordinate
def CalculateError(current, goal):
    # error is calculated using distance formula
    x = ((goal[0] - current[0])**2)+((goal[1] - current[1])**2)
    error = round(math.sqrt(x),2)   # round error to 2 digits after decimal
    return (error)



PivotLeft()
