# This test is successful

from picarx import Picarx
from time import sleep
from vilib import Vilib

px = Picarx()

def clamp_number(num,a,b):
    return max(min(num, max(a, b)), min(a, b))

def redLight():
    Vilib.camera_start()
    Vilib.display()      # display camera feed, can turn display off 
    Vilib.color_detect("red")
    speed = 50
    dir_angle=0
    x_angle =0
    y_angle =0
    while True:
        if Vilib.detect_obj_parameter['color_n']!=0:        # if red is detected
            coordinate_x = Vilib.detect_obj_parameter['color_x']
            coordinate_y = Vilib.detect_obj_parameter['color_y']
            # stop the car 
            print("Red light detected")
            
            return 1
        else:
            # go forward 
            return 0
            
            
def main():
    while redLight() == 0:
        px.forward(20)
    px.stop()
    
if __name__ == "__main__":
    try:
        main()

    finally:
        px.set_cam_pan_angle(0)
        px.set_cam_tilt_angle(0)
        px.stop()
        print("stop and exit")
        sleep(0.1)
