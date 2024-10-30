

from picarx import Picarx
import math
import time

car = Picarx()

# global parameters to change 
rightPower = 60     # this works when grayscale positions 
leftPower = 60
t = 1.5           # time to go straight
power = 30      # power to go straight
leftTime = 2.8    # time to pivot left 90 deg
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
        step = 0.2
        car.left(leftPower)
        time.sleep(step)
        car.backward(10)
        time.sleep(0.1)
        dummy+=step
        car.stop()

    car.stop()

def TurnWServo():
    global rightPower
    global rightTime
    global power 
    global t
    global leftPower
    global leftTime 
    car.set_dir_servo_angle(0)
    
    print("Turn right")
    car.set_dir_servo_angle(30)
    car.forward(20)
    time.sleep(1.3)
    car.stop()

# calibrating function
def GoStraight():
    t = 1.3     # per block 
    car.forward(30)
    time.sleep(t)
    car.stop()
    #car.left(50)
    #time.sleep(1.5)
    #car.stop()
    #car.forward(30)
    #time.sleep(t*2)
    #car.stop()
    return 

def car_forward():
    while True:
        gm_val_list = car.get_grayscale_data()
        while (gm_val_list[1] > 700):   # white line is on the middle
            car.forward(30)
        if (gm_val_list[0] > 700):  # white line is on the left 
            car.left(20)
            time.sleep(0.1)
            car_forward()
        elif (gm_val_list[2] > 700):    # line is on the right 
            car.right(20)
            time.sleep(0.1)
            car_forward()


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
    car_forward()
    

main()
car.set_cam_pan_angle(0)
