

from picarx import Picarx
import math
import time

car = Picarx()

# global parameters to change 
rightPower = 30
leftPower = 30
t = 1           # time to go straight
power = 50      # power to go straight
leftTime = 1.5    # time to pivot left 90 deg
rightTime = 1.5



# for pi3
def motors():
    car.stop()
    
    turnPower = 50
    right = 1.6
    left = 1
    t = 0
    # This method works -- can try another medthod of using rubber band
    # If rubber band does not work then can replicate the same for left pivot turn
    while (t <= right):
        car.right(turnPower)
        time.sleep(0.2)
        car.backward(30)
        time.sleep(0.1)
        t += 0.1
        car.stop()

    car.stop()

def test_turns():
    global rightPower
    global leftPower
    global leftTime 
    global rightTime
    global t 
    global power 

    car.stop()

    car.right(rightPower)
    car.sleep(rightTime)

    car.stop()
    time.sleep(1)

    car.left(rightPower)
    car.sleep(rightTime)


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
    motors()
    car.stop()
    car.set_cam_pan_angle(0)
    

main()
car.set_cam_pan_angle(0)
