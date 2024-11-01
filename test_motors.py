from picarx import Picarx
from time import sleep
import time
from vilib import Vilib
import math

px = Picarx()
px_power = 30
offset = 20
ref = 600
short = 0.85
long = 1.65     # time to travel 1 block 

def reset_dir_servo():
    px.set_dir_servo_angle(0)

def main():
    Vilib.camera_close()
    px.set_dir_servo_angle(30)
    time_max = time.time() + 3 
    while (time.time() <= time_max):
        gm_val_list = px.get_grayscale_data()
        for val in gm_val_list:
            if val > ref:   # if one of the sensors caught the line break the turnin loop 
                px.stop()
                break
            else:
                px.forward(20)
            break
        break
    reset_dir_servo()
                
  
reset_dir_servo()
main()
