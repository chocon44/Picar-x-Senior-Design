

from picarx import Picarx
import math
import time

car = Picarx()

# global parameters to change 
rightPower = 50
leftPower = 30
t = 1.5           # time to go straight
power = 30      # power to go straight
leftTime = 1    # time to pivot left 90 deg
rightTime = 2.6




def motors_testing():
    global rightPower
    global leftPower
    global leftTime 
    global rightTime
    global t 
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

def test_turns():
    global rightPower
    global leftPower
    global leftTime 
    global rightTime
    global t 
    global power 

    car.stop()

    car.forward(power)
    time.sleep(t)

    car.backward(power)
    time.sleep(t)
    
    

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
    motors_testing()
    car.stop()
    car.set_cam_pan_angle(0)
    

main()
car.set_cam_pan_angle(0)
