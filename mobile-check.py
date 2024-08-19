from picarx import Picarx
import time



power = 70


def reset_turn_servo():
    global power
    time.sleep(0.2)
    car.forward(0)  # stop the car
    car.set_dir_servo_angle(0)  # reset servo angle to 0
    time.sleep(0.2)

def turn_right():
    global power
    car.forward(0)  # stop the car
    car.set_dir_servo_angle(40) # rotate servo angle to the right
    car.forward(power) # go forward for 1 sec
    time.sleep(0.5)
    reset_turn_servo()  # reset turning angle back to 0


def turn_left():
    global power
    car.forward(1)  # stop the car
    car.set_dir_servo_angle(-40)    # turn servo to left turn
    car.forward(power)
    time.sleep(0.5) # pause for half a second then reset servo angle to go straight
    reset_turn_servo()


def main():
    car.forward(power)
    time.sleep(1.25*2)

    #turn_left()

    #car.forward(power)
    #time.sleep(1)
    
    car.forward(0)

car=Picarx()
main()

    

