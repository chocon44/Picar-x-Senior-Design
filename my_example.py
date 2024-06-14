## SIMPLE MOVING EXAMPLE
## THE FOLLOWING CODE IS TO DEMONSTRATE SIMPLE FORWARD AND TURNING MOVEMENT
## 

from picarx import Picarx
import time



power = 30


# This function returns target destination coordinates for the car [x,y] 
def get_final_coord():
    end = [3,5]
    return end

# This function returns intial coordinates for the car, assume (0,0) for now
# Assume (0,0) is the left bottom corner for the grid
def get_initial_coord():
    start = [0,0]
    return start

# This function resets the turning servo of the car back to 0
# Front wheels to be heading forward
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
    time.sleep(1)
    reset_turn_servo()  # reset turning angle back to 0 



def main():
    global power
    reset_turn_servo()
    
    # Reading start and end coordinates
    initial = get_initial_coord()
    final = get_final_coord()
    # define initial x and y
    yi = initial[1] 
    xi = initial[0]
    # define final x and y
    xf = final[0]
    yf = final[1]
    # initialize current x and y 
    currx = 0
    curry = 0
    
    # test printing
    print("Initial coordinate: " , "(" , xi, ",", yi, ")")

    # traverse y direction first
    while (curry != yf):

        ydiff = yf - curry 
        while (ydiff > 0):
            car.forward(power)
            time.sleep(1)
            ydiff -= 1
            curry += 1
            print("Current coordinate: ", "(", currx , "," , curry, ")")


    # traverse x direction
    while (currx != xf):
        xdiff = xf - currx
        time.sleep(0.5)
        turn_right()
        while (xdiff > 0):
            car.forward(power)
            time.sleep(1)
            xdiff -=1
            currx +=1
            print("Current coordinate: ", "(", currx , "," , curry, ")")
 
   # EXTRA RIGHT TURN
   # car.forward(power)
   # time.sleep(1)

   # turn_right()
   # time.sleep(0.5)

   # car.forward(30)
   # time.sleep(2)


    

try:
    car = Picarx()
    main()
finally:
    car.forward(0)  # stop the car
