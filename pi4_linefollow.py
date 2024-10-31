# This code is done for picar 4

from picarx import Picarx
from time import sleep
import time
from vilib import Vilib

px = Picarx()
px_power = 30
offset = 20
ref = 600
# px = Picarx(grayscale_pins=['A0', 'A1', 'A2'])

#px.set_line_reference([1400, 1400, 1400])


def go_forward(max_time):
    Vilib.camera_close()
    max_time = time.time() + 1.3  # set max time 
    # go straight
    while (time.time() < max_time):
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

def go_forward_again():
    Vilib.camera_close()
    max_time = time.time() + 1.5  # set max time 
    # go straight
    while (time.time() < max_time):
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


def Forward():

    def RedLight():  
        Vilib.camera_start()
        #Vilib.display()        # toggle display on when needed
        Vilib.color_detect("red")
        # red signal detect
        if Vilib.detect_obj_parameter['color_n']!=0:    # if red is detected
            print("Red light detected")
            px.stop()      # stop the car immediately
            Vilib.camera_close()
            
            # TESTING PURPOSE push redlight result to firebase
            # data = {
            # "Redlight detected": 1}
            # database.child("Picarx4").child("Red light detected").set(data)
            
            px.stop()
            time.sleep(1)
            RedLight()      # check red light again

    go_forward()

    # check for traffic light before moving to the next block 
    #RedLight()

    go_forward_again()
    # start turningg here, check for light and obstacle
    #RedLight()
    #ObstacleSweep()
    
    #px.left(50)
    #time.sleep(1.3)

    # go forward for 1 more block
    #go_forward(1.5)


    px.stop()
    px.set_dir_servo_angle(0)


def ObstacleAhead():
    Vilib.camera_close()
    danger = 10
    dist = round(px.ultrasonic.read(),2)
    Vilib.camera_close()
    if (dist > 0) and (dist <= danger):      # if obstacle is detected closely
        px.stop()          # stop the px 
        print("Obstacle detected at: ", dist)
        time.sleep(2)       # wait 2 seconds before checking again 
        ObstacleAhead()     # repeat this function until the obstacle is cleared
    return


def ObstacleSweep():
    Vilib.camera_close()
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
            px.stop()          # stop the car 
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
            px.stop()          # stop the car 
            print("Obstacle detected at: ", dist)
            obsAngle = angle    # note the angle obstacle is detected
            time.sleep(waitTime)       # wait 2 seconds before checking again 
            ObstacleSweep()     # repeat this function until the obstacle is cleared
        else:   # when no close obstacle is detected, do nothing
            pass
        angle -= 10
    px.set_cam_pan_angle(0)        # reset pan servo angle at the end    
    return



def main():
    max_time = time.time() + 10
    while time.time() < max_time:
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
    px.set_dir_servo_angle(0)

Forward()