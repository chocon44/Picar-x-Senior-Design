#NOTES: ADDED ATTRIBUTE TO ROOT FILE AND RE-INSTALLED, LEFT AND RIGHT FUNCTIONS WORKED,
# ANGLES DEPEND ON TIME.SLEEP()
from picarx import Picarx
import math
import time



def test_motors():
    car = Picarx()
    
    car.left(30)
    time.sleep(2)
    car.stop()
    time.sleep(1)
    car.right(30)
    time.sleep(1.8)
    car.stop()

def ultra():
    car = Picarx()
    angle = -90
    while (angle <= 90):
        car.set_cam_ultra_angle(angle)
        time.sleep(0.5)
        angle += 10

def main():
    
    #test_motors()
    ultra()

main()
car = Picarx()
car.stop()
