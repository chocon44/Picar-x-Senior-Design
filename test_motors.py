
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


main()
car = Picarx()
car.stop()
