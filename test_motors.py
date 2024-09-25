#NOTES: ADDED ATTRIBUTE TO ROOT FILE AND RE-INSTALLED, LEFT AND RIGHT FUNCTIONS WORKED,
# ANGLES DEPEND ON TIME.SLEEP()
from picarx import Picarx
import math
import time

def main():
    car = Picarx()
    #car.forward(30)
    #time.sleep(1)
    car.left(30)
    time.sleep(2)
    car.stop()
    time.sleep(1)
    car.right(30)
    time.sleep(1.8)
    car.stop()

main()
car = Picarx()
car.stop()
