from picarx import Picarx
import math
import time

car = Picarx()
def motors():
    car.right(70)
    time.sleep(2)
    car.stop()
    time.sleep(1)
    car.left(70)
    time.sleep(2)
    car.stop()

def ultra():
    car.set_cam_ultra_angle(0)
    time.sleep(3)
    angle = -90
    while (angle <= 90):
        car.set_cam_ultra_angle(angle)
        time.sleep(0.2)
        angle += 10
    while (angle >= -90):
        car.set_cam_ultra_angle(angle)
        time.sleep(0.2)
        angle -= 10
    car.set_cam_ultra_angle(0)

def main():
    #motors()
    ultra()
    car.stop()

main()
