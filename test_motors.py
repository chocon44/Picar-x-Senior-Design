

from picarx import Picarx
import math
import time

car = Picarx()

# global parameters to change 
rightPower = 60     # this works when grayscale positions 
leftPower = 30
t = 1.5           # time to go straight
power = 30      # power to go straight
leftTime = 1    # time to pivot left 90 deg
rightTime = 2.6




def Turn_Right():
    global rightPower
    global rightTime
    global power 

    car.stop() 

    # This method works -- can try another medthod of using rubber band
    dummy = 0
    while (dummy <= rightTime):
        step = 0.3
        car.right(rightPower)
        time.sleep(step)
        car.backward(20)
        time.sleep(0.1)
        dummy+=step
        car.stop()

    car.stop()

def Turn_Left():
    global leftPower
    global leftTime 
    global power 

    car.stop() 

    # This method works -- can try another medthod of using rubber band
    dummy = 0
    while (dummy <= leftTime):
        step = 0.3
        car.left(leftPower)
        time.sleep(step)
        car.backward(20)
        time.sleep(0.1)
        dummy+=step
        car.stop()

    car.stop()


def read_ultrasonic():
    dist = round(car.ultrasonic.read(),2)
    print("Distance to obstacle: ", dist)
    if (dist >= 40):
        return 0
    else:
        return 1

def test_ultrasonic():
    while True:
        dist = round(car.ultrasonic.read(),2)
        print("Distance to obstacle: ", dist)
    
    

# ultrasonic attached to pan servo
def pan_sonic():
    car.set_cam_pan_angle(0)
    time.sleep(0.5)
    angle = -50
    while (angle <= 50):
        car.set_cam_pan_angle(angle)
        time.sleep(1)
        # read ultrasonic 
        if  (read_ultrasonic() == 1):
            print("Obstacle detected")
            car.stop()
            car.set_cam_pan_angle(angle)
            return angle
        angle += 10
    while (angle >= -50):
        car.set_cam_pan_angle(angle)
        time.sleep(1)
        if  (read_ultrasonic() == 1):
            print("Obstacle detected")
            car.stop()
            car.set_cam_pan_angle(angle)
            return angle
        angle -= 10
    

def pan():
    car.set_cam_pan_angle(0)
    time.sleep(1)
    angle = -50
    while (angle <= 50):
        car.set_cam_pan_angle(angle)
        time.sleep(0.2)
        angle += 10
    while (angle >= -50):
        car.set_cam_pan_angle(angle)
        time.sleep(0.2)
        angle -= 10
    car.set_cam_pan_angle(0)





def main():
    Turn_Left()
    car.stop()
    car.set_cam_pan_angle(0)
    

main()
car.set_cam_pan_angle(0)
