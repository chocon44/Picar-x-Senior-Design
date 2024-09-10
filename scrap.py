from picarx import Picarx
from robot_hat import Motors
import math
import time



def Forward():
    global motors
    global LEFT
    global RIGHT
    motors[LEFT].speed(-50)
    motors[RIGHT].speed(70)

Forward()
time.sleep(1)
