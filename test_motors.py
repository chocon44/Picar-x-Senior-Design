from picarx import Picarx
import math
import time

car = Picarx()

# for pi3
def motors():
    car.stop()
    
    turnPower = 50
    right = 1.6
    left = 1
    t = 0
    
    while (t <= right):
        car.right(turnPower)
        time.sleep(0.2)
        car.backward(30)
        time.sleep(0.1)
        t += 0.1
        car.stop()

    #car.left(turnPower)
    #time.sleep(left)
    car.stop()

# def ultra():
    # car.set_cam_ultra_angle(0)
    # time.sleep(1)
    # angle = -90
    # while (angle <= 90):
        # car.set_cam_ultra_angle(angle)
        # time.sleep(0.2)
        # angle += 10
    # while (angle >= -90):
        # car.set_cam_ultra_angle(angle)
        # time.sleep(0.2)
        # angle -= 10
    # car.set_cam_ultra_angle(0)

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
