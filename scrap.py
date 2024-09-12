# Note: 1.25 sec for 1 grid
# Last updated 9/12

from picarx import Picarx
#from robot_hat import Motors
import math
import time


path = []
power = 30      # standard power for car going straight 
rightTurnPower = 10
rightTurnTime = 0.7
leftTurmPower = 10
leftTurnTime = 0.7

def LaneCheck():   
   
    print("Lane check")
    
    # read data from grayscale
    gm_val_list = car.get_grayscale_data()
        
    # re-orient the car based on grayscale reading 
    
    #xxo, xoo
    if (gm_val_list[0] < 200):    # the black line is on the left of the car, move right 
        car.forward(0)  # stop the car
        car.set_dir_servo_angle(20) # rotate servo angle to the right
        car.forward(power) # go forward for 1 sec
        time.sleep(0.1)   # CHANGED FROM 0.5
        reset_turn_servo()  # reset turning angle back to 0
    #oxx, oox
    elif (gm_val_list[2] < 200):    # the black line is on the right of the car, move left 
        car.forward(0)  # stop the car 
        car.set_dir_servo_angle(-20)    # turn servo to left turn 
        car.forward(power)  
        time.sleep(0.1) # pause for half a second then reset servo angle to go straight
        reset_turn_servo()
    #xxx, oxo
    #else:


def slow_turn_right():
    global power 
    global rightTurnPower
    global rightTurnTime
    
    totalTime = rightTurnTime
    car.forward(0)  # stop the car 
    car.set_dir_servo_angle(30) # rotate servo angle to the right 
      
    # # as long as there is no obstacle in the front, continue turning until totalTime is reached
    # while (ObstacleCheck() == 0):   
        # car.forward(rightTurnPower)
        # time.sleep(0.1)
        # totalTime -= 0.1
        # if (totalTime == 0):
            # break       # finish loop when total rightTurnTime has been reached
    # # if obstacle is detected...
    # else:
        # reset_turn_servo() 
        # car.forward(power)
        # time.sleep(0.5)
        # car.forward(0)
    
    while (totalTime != 0):
        car.forward(rightTurnPower)
        time.sleep(0.1)
        LaneCheck()
        totalTime -= 0.1
        
    

def slow_turn_left():
    global power 
    global leftTurnPower
    global leftTurnTime
    
    totalTime = turnLeftTime
    car.forward(0)
    car.set_dir_servo_angle(-30)    # turn servo to left turn  
    
    # # as long as there is no obstacle in the front, continue turning until totalTime is reached
    # while (ObstacleCheck() == 0):   
        # car.forward(leftTurnPower)
        # time.sleep(0.1)
        # totalTime -= 0.1
        # if (totalTime == 0):
            # break       # finish loop when total leftTurnTime has been reached
    # # if obstacle is detected...
    # else:
        # reset_turn_servo() 
        # car.forward(power)
        # time.sleep(0.5)
        # car.forward(0)
    
    while (totalTime != 0):
        car.forward(leftTurnPower)
        time.sleep(0.1)
        LaneCheck()
        totalTime -= 0.1

<<<<<<< HEAD
<<<<<<< HEAD
motors = Motors() 
# identify each motor
LEFT = 1
RIGHT = 2

def Forward():
    global motors
    global LEFT
    global RIGHT
    motors[LEFT].speed(-50)
    motors[RIGHT].speed(70)

def PivotRight():
    global motors
    global LEFT
    global RIGHT
    motors[LEFT].speed(-60)
    motors[RIGHT].speed(-70)
    time.sleep(2.2)    # for 90 degrees, may change with time
    motors.stop()

def PivotLeft():
    global motors
    global LEFT
    global RIGHT
    motors[LEFT].speed(70)
    motors[RIGHT].speed(70)
    time.sleep(2)
    motors.stop()

Forward()
time.sleep(1.25*2.5)
motors.stop()
PivotRight()
motors.stop()
=======
car = Picarx()
slow_turn_left()
car.forward(0)
>>>>>>> 9be038493edd21a26401f870cf2416b44f12d89c
=======

def main():
   slow_turn_left()

try:
    car = Picarx()
    main()

finally:
    car.forward(0)
>>>>>>> 78ebe281c32c90049e3e356f7fb22366175074db
