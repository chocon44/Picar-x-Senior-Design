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
        time.sleep(0.5)
        angle += 10

flag_color = True
def camera():
    global flag_color
    
    Vilib.camera_start(vflip=False,hflip=False)
    Vilib.display(local=True,web=True)
    print(manual)

    if flag_color is True:
        if Vilib.detect_obj_parameter['color_n'] == 0:
            print('Color Detect: None')
        else:
            color_coodinate = (Vilib.detect_obj_parameter['color_x'],Vilib.detect_obj_parameter['color_y'])
            color_size = (Vilib.detect_obj_parameter['color_w'],Vilib.detect_obj_parameter['color_h'])
            print("[Color Detect] ","Coordinate:",color_coodinate,"Size",color_size)


def main():
    car = Picarx()
    #test_motors() 
    #ultra() 
    camera()

main()

car.stop()
