# Note: 1.25 sec for 1 grid
# Last updated 9/10


from robot_hat import Motors

import time

motors = Motors() 
# identify each motor
LEFT = 1
RIGHT = 2

def Forward():
    global motors
    global LEFT
    global RIGHT
    motors[LEFT].speed(-50)
    motors[RIGHT].speed(70)

def PivotRight():
    global motors
    global LEFT
    global RIGHT
    motors[LEFT].speed(-70)
    motors[RIGHT].speed(-70)
    time.sleep(2.2)    # for 90 degrees, may change with time
    motors.stop()

def PivotLeft():
    global motors
    global LEFT
    global RIGHT
    motors[LEFT].speed(70)
    motors[RIGHT].speed(70)
    time.sleep(1.6)
    motors.stop()

Forward()
time.sleep(1.25*2)
motors.stop()
PivotRight()
motors.stop()
