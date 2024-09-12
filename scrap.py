# Note: 1.25 sec for 1 grid
# Last updated 9/12

from picarx import Picarx
#from robot_hat import Motors
import math
import time


path = []
power = 30      # standard power for car going straight 
rightTurnPower = 5
rightTurnTime = 0.7
leftTurnPower = 5
leftTurnTime = 0.7


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
    if (gm_val_list[0] < 300) or (gm_val_list[2] < 200):    # the black line is on the left of the car, move right 
        # stop turning    
        reset_turn_servo()
        return 1
    else:
        return 0


def slow_turn_right():
    global power 
    global rightTurnPower
    global rightTurnTime
    
    totalTime = rightTurnTime
    car.forward(0)  # stop the car 
    car.set_dir_servo_angle(30) # rotate servo angle to the right 
      
    # # as long as there is no obstacle in the front, continue turning until totalTime is reached
    while (LaneCheck() == 0):   
         car.forward(rightTurnPower)
         time.sleep(0.1)
         totalTime -= 0.1
         if (totalTime == 0):
             break       # finish loop when total rightTurnTime has been reached
    # # if lane is detected...
    else:
        reset_turn_servo() 
        car.forward(power)
        time.sleep(0.5)
        car.forward(0)
    
        
    

def slow_turn_left():
    global power 
    global leftTurnPower
    global leftTurnTime
    
    totalTime = leftTurnTime
    car.forward(0)  # stop the car 
    car.set_dir_servo_angle(-30) # rotate servo angle to the left 
      
    # # as long as there is no obstacle in the front, continue turning until totalTime is reached
    while (totalTime != 0):
        car.forward(leftTurnPower)
        time.sleep(0.1)
        if (LaneCheck() == 0):
            totalTime -=0.1
        else:
            totalTime == 0
            break
    reset_turn_servo()
    car.forward(0)

    #while (LaneCheck() == 0):   
         #car.forward(leftTurnPower)
         #time.sleep(0.1)
         #totalTime -= 0.1
         #if (totalTime == 0):
             #break       # finish loop when total rightTurnTime has been reached
    # # if lane is detected...
    #else:
        #reset_turn_servo() 
        #car.forward(leftTurnPower)
        #time.sleep(0.5)
        #car.forward(0)

def main():
    slow_turn_left()
    car.forward(0)

car = Picarx()
main()