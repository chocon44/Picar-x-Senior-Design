
from picarx import Picarx
import math
import time

def main():
    car = Picarx()
    car.forward(30)
    time.sleep(1)
    #car.PivotRight(30)
    #time.sleep(1)
    car.stop()

car = Picarx()
main()
