#NOTES: ADDED ATTRIBUTE TO ROOT FILE AND RE-INSTALLED, LEFT AND RIGHT FUNCTIONS WORKED,
# ANGLES DEPEND ON TIME.SLEEP()
from picarx import Picarx
import math
import time

def test_ultra():
    car = Picarx()
    #car.set_cam_pan_angle(x_angle)
    #car.set_cam_ultra_angle(90)
    #time.sleep(1)
    #car.set_cam_ultra_angle(-90)

def test_motors():
    car = Picarx()
    
    car.left(30)
    time.sleep(2)
    car.stop()
    time.sleep(1)
    car.right(30)
    time.sleep(1.8)
    car.stop()

def main():
    car = Picarx()
    
    test_motors()
    #test_ultra()

main()
car = Picarx()
car.stop()
