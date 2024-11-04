# This code is done for picar 4
# Go straight for 1 blocks, then turn left
# Car will start at intersection 
# Turned off camera to adjust speed

from picarx import Picarx
from time import sleep
import time
#from vilib import Vilib
import math

px = Picarx()
px_power = 20           # just changed
offset = 20
ref = 500
short = 0.8
long = 6     # time to travel 1 block 

# px = Picarx(grayscale_pins=['A0', 'A1', 'A2'])

#px.set_line_reference([1400, 1400, 1400])


def go_forward():
    max_time = time.time() + long    # time to travel 1 block, starting from intersection 
    while (time.time() < max_time):
        ObstacleAhead()     # scan for obstacle ahead
        gm_val_list = px.get_grayscale_data()
        if gm_val_list[1] > ref:
            px.set_dir_servo_angle(0)
            px.forward(px_power)

        elif (gm_val_list[0] > ref) and (gm_val_list[1] > ref) and (gm_val_list[2] > ref):
            px.set_dir_servo_angle(0)
            px.forward(px_power)
        elif gm_val_list[0] > ref:   # line is on the left -- move right
            px.set_dir_servo_angle(-offset)
            px.forward(px_power)
        elif gm_val_list[2] > ref:   # line is on the right -- move left
            px.set_dir_servo_angle(offset)
            px.forward(px_power)
        else:
            px.stop()
    px.stop()
    return 

def go_forward_short():
    max_time = time.time() + short
    while (time.time() < max_time):
        ObstacleAhead()     # scan for obstacle ahead
        gm_val_list = px.get_grayscale_data()
        if gm_val_list[1] > ref:
            px.set_dir_servo_angle(0)
            px.forward(px_power)

        elif (gm_val_list[0] > ref) and (gm_val_list[1] > ref) and (gm_val_list[2] > ref):
            px.set_dir_servo_angle(0)
            px.forward(px_power)
        elif gm_val_list[0] > ref:   # line is on the left -- move right
            px.set_dir_servo_angle(-offset)
            px.forward(px_power)
        elif gm_val_list[2] > ref:   # line is on the right -- move left
            px.set_dir_servo_angle(offset)
            px.forward(px_power)
        else:
            px.stop()
    px.stop()
    return 

def turn_right():
    
    #time_max = time.time() + 3      # max turning time is 2 sec 
    
    #while (time.time() <= time_max):
    #    px.set_dir_servo_angle(30)
    #    px.forward(10)
    #    gm_val_list = px.get_grayscale_data()
        # check if grayscale is getting the line 
    #    for val in gm_val_list:
    #        if val > ref:   # if one of the sensors caught the line break the turnin loop 
    #            break
    #    break 
    
    px.set_dir_servo_angle(30)
    print("Angle set")



    return 


# this function is used to detected obstacles at intersections by sweeping ultrasonic sensor 
# 100 degrees left to right 
def ObstacleSweep():
    px.set_cam_pan_angle(0)    # reset pan servo angle 
    time.sleep(0.5)
    angle = -50     # initialize to -50 deg
    danger = 10
    sweepTime = 0.1
    waitTime = 0.2    # time to read inputs again
    while (angle <= 50):
        px.set_cam_pan_angle(angle)
        time.sleep(sweepTime)
        # read ultrasonic sensor value 
        dist = round(px.ultrasonic.read(),2)
        if (dist > 0) and (dist <= danger):      # if obstacle is detected closely
            px.stop()          # stop the px 
            print("Obstacle detected at: ", dist)
            obsAngle = angle    # note the angle obstacle is detected
            time.sleep(waitTime)       # wait 2 seconds before checking again 
            ObstacleSweep()     # repeat this function until the obstacle is cleared
        else:   # when no close obstacle is detected, do nothing
            pass
        angle += 10
    # do the same thing on the other side 
    while (angle >= -50):
        px.set_cam_pan_angle(angle)
        time.sleep(sweepTime)
        # read ultrasonic sensor value 
        dist = round(px.ultrasonic.read(),2)
        if (dist > 0) and (dist <= danger):        # if obstacle is detected closely
            px.stop()          # stop the px 
            print("Obstacle detected at: ", dist)
            obsAngle = angle    # note the angle obstacle is detected
            time.sleep(waitTime)       # wait 2 seconds before checking again 
            ObstacleSweep()     # repeat this function until the obstacle is cleared
        else:   # when no close obstacle is detected, do nothing
            pass
        angle -= 10
    px.set_cam_pan_angle(0)        # reset pan servo angle at the end    
    return
    
    
# This function is used to detect other cars when going straight
#def ObstacleAhead():
#    danger = 10
#    dist = round(px.ultrasonic.read(),2)
    #Vilib.camera_close()
#    if (dist > 0) and (dist <= danger):      # if obstacle is detected closely
#        px.stop()          # stop the car 
#        print("Obstacle detected at: ", dist)
#        time.sleep(1)       # wait 1 sec before checking again 
#        ObstacleAhead()     # repeat this function until the obstacle is cleared
#    return
    
    
# This function starts camera to check for red light
#def RedLight():  
#    Vilib.camera_start()
#    #Vilib.display()        # toggle display on when needed
#    Vilib.color_detect("red")
    # red signal detect
#    if Vilib.detect_obj_parameter['color_n']!=0:    # if red is detected
#        print("Red light detected")
#        px.stop()      # stop the car immediately
#        time.sleep(0.5)   
#        RedLight()      # check red light again 
#    else:        # if red is not detected -- green or yellow
#        Vilib.camera_close()
#        return    


def main():
    try: 
        go_forward()

        #px.left(30)
        #time.sleep(1.5)
        #px.stop()
        #time.sleep(0.02)
        #go_forward()



    finally:
        px.stop()


if __name__ == "__main__":
    main()