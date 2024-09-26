#NOTES: ADDED ATTRIBUTE TO ROOT FILE AND RE-INSTALLED, LEFT AND RIGHT FUNCTIONS WORKED,
# ANGLES DEPEND ON TIME.SLEEP()
# ADDED ULTRA SERVO SUCCESSFULLY

from vilib import Vilib
from picarx import Picarx
import math
import time


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

def camera():
    Vilib.camera_start()
    Vilib.display()
    Vilib.color_detect("red")
    if Vilib.detect_obj_parameter['color_n']!=0:
        coordinate_x = Vilib.detect_obj_parameter['color_x']
        coordinate_y = Vilib.detect_obj_parameter['color_y']

        # change the pan-tilt angle for track the object
        x_angle +=(coordinate_x*10/640)-5
        x_angle = clamp_number(x_angle,-35,35)
        car.set_cam_pan_angle(x_angle)

        y_angle -=(coordinate_y*10/480)-5
        y_angle = clamp_number(y_angle,-35,35)
        car.set_cam_tilt_angle(y_angle)


def main():
    car = Picarx()
    #test_motors() 
    #ultra() 
    camera()

main()

car.stop()
