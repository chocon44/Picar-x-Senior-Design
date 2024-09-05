# Last updated: 8/26
# Notes: 1) See calibration.py for more examples 2) Testing grayscale module to detect color white to keep car in lane 3) Testing ultrasonic sensor to avoid obstacle 4) Testing color recognition

from picarx import Picarx
import time
from vilib import Vilib

power = 30
turningPower = 30     # To adjust better turning angle

car = Picarx()



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


def Color_Testing():
    global power 
    
    reset_turn_servo()
    
    Vilib.camera_start()    # start camera
    Vilib.display()    # display camera feed
    # Enable color detection and specify target as "red"
    Vilib.color_detect("red")   

    while True:
        # check if the color red is detected 
        if Vilib.detect_obj_parameter['color_n'] != 0:
            
            # Coordinate x and y are for tilting camera servo, these are coordinates of the red color detected
            coordinate_x = Vilib.detect_obj_parameter['color_x']
            coordinate_y = Vilib.detect_obj_parameter['color_y']

            # When red is detected, the car will stop
            car.forward(0)    # stop the car when red is detected

        else:    # if red is not detected, the car will continue going straight
            car.forward(power) # go straight if there is no red


def Obstacle_Testing():
    global power
    reset_turn_servo()
    safeDistance = 40    # distance higher than 40 is safe
    dangerDistance = 20    # distance between 20 and 40 is dangerous
    while True:
        # read ultrasonic sensor distance and round it 
        distance = round(car.ultrasonic.read(),2)    
        print("Distance to obstacle = ", distance)

        if (distance >= safeDistance):
            car.forward(power)    # go straight if in safe distance
        elif distance >= dangerDistance:
            car.forward(0)    # stop otherwise
        else:
            car.forward(0)

def Grayscale_Testing():
    global power
    reset_turn_servo()
    # read data from grayscale
    gm_val_list = px.get_grayscale_data()

    for i in range(len(3)):
        print(gm_val_list[i], end = ' ')


def main():
    Grayscale_Testing()
    
    
    
            

if __name__ == "__main__":
    try:
        main()
    finally:
        car.forward(0)
        



# Outside of main() function 
# car=Picarx()
# main()

    

