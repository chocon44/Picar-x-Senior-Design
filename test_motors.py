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


def main():
    Vilib.camera_close()
    px.set_dir_servo_angle(30)
  


main()
px.set_dir_servo_angle(0)
