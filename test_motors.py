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
    time.sleep(0.5))
    angle = -90
    while (angle <= 70):
        car.set_cam_pan_angle(angle)
        time.sleep(1)
        # read ultrasonic 
        if  (read_ultrasonic() == 1):
            print("Obstacle detected")
            car.stop()
            car.set_cam_pan_angle(angle)
            return angle
        angle += 10
    while (angle >= -70):
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
    angle = -90
    while (angle <= 90):
        car.set_cam_pan_angle(angle)
        time.sleep(0.2)
        angle += 10
    while (angle >= -90):
        car.set_cam_pan_angle(angle)
        time.sleep(0.2)
        angle -= 10
    car.set_cam_pan_angle(0)

def main():
    #motors()
    #ultra()
    obstacleAngle = pan_sonic()
    print ("Obstacle at angle: ", obstacleAngle)
    #test_ultrasonic()
    car.stop()
    car.set_cam_pan_angle(0)
    

main()
car.set_cam_pan_angle(0)
