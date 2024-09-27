#NOTES: ADDED ATTRIBUTE TO ROOT FILE AND RE-INSTALLED, LEFT AND RIGHT FUNCTIONS WORKED,
# ANGLES DEPEND ON TIME.SLEEP()
# ADDED ULTRA SERVO SUCCESSFULLY

from vilib import Vilib
from picarx import Picarx
import math
import time

from pydoc import text

import threading
import readchar
import os


car = Picarx()

def test_motors():  # passed
    car = Picarx()
    
    car.left(30)
    time.sleep(2)
    car.stop()
    time.sleep(1)
    car.right(30)
    time.sleep(1.8)
    car.stop()

def ultra():    # passed
    car = Picarx()
    time.sleep(3)
    angle = -90
    while (angle <= 90):
        car.set_cam_ultra_angle(angle)
        #time.sleep(0.5)
        angle += 10
    time.sleep(1)
    while(angle >= -90):
        car.set_cam_ultra_angle(angle)
        angle -=10




def main():
    car = Picarx()
    #test_motors() 
    ultra() 
    #camera()

main()

car.stop()
