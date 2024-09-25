#NOTES: ADDED ATTRIBUTE TO ROOT FILE AND RE-INSTALLED, LEFT AND RIGHT FUNCTIONS WORKED,
# ANGLES DEPEND ON TIME.SLEEP()
from picarx import Picarx
import math
import time

def test_ultra():
    car = Picarx()
    car.set_cam_ultra_angle(90)
    time.sleep(1)
    car.set_cam_ultra_angle(-90)

def main():
    car = Picarx()
    
    #car.left(30)
    #time.sleep(2)
    #car.stop()
    #time.sleep(1)
    #car.right(30)
    #time.sleep(1.8)
    #car.stop()

    test_ultra()

main()
car = Picarx()
car.stop()
