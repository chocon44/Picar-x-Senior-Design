# This file is created to test inputing different power level to each motor
# Last updated: 9/10

from picarx import Picarx
from robot_hat import Motors
import time




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

def LaneCheck():
    
    print("Lane check")
    car = Picarx()
    
    # read data from grayscale
    gm_val_list = car.get_grayscale_data()
    return gm_val_list

PivotLeft()
