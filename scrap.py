# Note: 1.25 sec for 1 grid
# Last updated 9/17

from picarx import Picarx
#from robot_hat import Motors
import math
import time


path = []
power = 30      # standard power for car going straight 
rightTurnPower = 5
rightTurnTime = 0.7
rightTurnAngle = 50

leftTurnPower = 5
leftTurnTime = 0.7
leftTurnAngle = -70


# This function resets the turning servo of the car back to 0
# Front wheels to be heading forward
def reset_turn_servo():
    global power
    time.sleep(0.2)
    car.forward(0)  # stop the car
    car.set_dir_servo_angle(0)  # reset servo angle to 0
    time.sleep(0.2)


def LaneCheck():   
   
    print("Lane check")
    
    # read data from grayscale
    gm_val_list = car.get_grayscale_data()
        
    #xxo, xoo
    if (gm_val_list[0] < 300):    # the black line is on the left of the car, move right 
        # stop turning    
        print("Sensor [0] detected - line on the right")
        reset_turn_servo()
        return 0
    elif (gm_val_list[2] < 300): 
        # stop turning    
        print("Sensor [2] detected - line on the left")
        reset_turn_servo()
        return 2
    else:
        return 4


# Experimenting this right now... sep 12
def slow_turn_left():
    global power 
    global leftTurnPower
    global leftTurnTime
    
    totalTime = leftTurnTime
    car.forward(0)  # stop the car 
    car.set_dir_servo_angle(-50) # rotate servo angle to the left 
      
    # # as long as there is no obstacle in the front, continue turning until totalTime is reached
    while (totalTime != 0):
        car.forward(leftTurnPower)
        time.sleep(0.1)
        totalTime -= 0.1
        if (LaneCheck() == 4):    # no lane detected
            car.forward(leftTurnPower)
        elif (LaneCheck() == 0):    # sensor 0 detected line - go left 
            print()
        elif (LaneCheck() == 2):    # sensor 2 detected line - go right
            print()
            #car.set_dir_servo_angle(30)
            #car.forward(leftTurnPower)
        else:
            totalTime == 0
            car.forward(0)
            break
    reset_turn_servo()
    car.forward(0)


def turn_left():
    global leftTurnTime
    global leftTurnPower
    
    car.forward(0)  # stop the car 
    car.set_dir_servo_angle(-70) # rotate servo angle to the left 
    car.forward(leftTurnPower)
    time.sleep(10)

def main():
    turn_left()
    car.set_dir_servo_angle(0)  # reset turning servo
    car.forward(0)
    

car = Picarx()
main()
