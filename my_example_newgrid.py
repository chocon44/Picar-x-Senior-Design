
 
#-----------------
# CODE FROM MY-EXAMPLE
#
# LAST UPDATED: 9/2/24 
#
# DESCRIPTION: PATH SEARCHING TESTING
#   
# NOTES: New grid implemented
#-----------------

from picarx import Picarx
import time
import math

path = []
power = 40

# This function returns the target destination 
# Returns a list of x,y
def get_final_coord():  
    endx = int(input("Enter destination x coordinate: "))
    endy = int(input("Enter destination y coordinate: "))
    end = [endx,endy]
    return end
    
# This function returns the starting position 
# Returns a list of x,y
def get_initial_coord():
    startx = int(input("Enter starting x coordinate: "))
    starty = int(input("Enter starting y coordinate: "))
    start = [startx,starty]
    return start


# This function resets the turning servo of the car back to 0
# Front wheels to be heading forward
def reset_turn_servo():
    global power
    time.sleep(0.2)
    car.forward(0)  # stop the car
    car.set_dir_servo_angle(0)  # reset servo angle to 0
    time.sleep(0.2)

# Turn right and left functions tilt the front wheels to 
# respective direction, go forward then reset the 
# front wheels back to its original position (heading forward)
def turn_right():
    global power
    car.forward(0)  # stop the car
    car.set_dir_servo_angle(40) # rotate servo angle to the right
    car.forward(power) # go forward for 1 sec
    time.sleep(1)   # CHANGED FROM 0.5
    reset_turn_servo()  # reset turning angle back to 0

def turn_left():
    global power
    car.forward(0)  # stop the car 
    car.set_dir_servo_angle(-40)    # turn servo to left turn 
    car.forward(power)  
    time.sleep(1) # pause for half a second then reset servo angle to go straight
    reset_turn_servo()




# This function returns error value in respect with the goal coordinate
def CalculateError(current, goal):
    # error is calculated using distance formula
    x = ((goal[0] - current[0])**2)+((goal[1] - current[1])**2)
    error = round(math.sqrt(x),2)   # round error to 2 digits after decimal
    return (error)



path = []
# This function returns a list of coordinates the car needs to travel to get
# to the input goal location
def GetPath(current, goal):
    
    # this stores the coordinates of path, in order
    global path
    
    xc = current[0]
    yc = current[1]
    xGoal = goal[0]
    yGoal = goal[1]
    
    # flags for directions
    down = 0    # y - 2
    up = 0      # y + 2
    left = 0    # x - 2
    right = 0   # x + 2
    
    # empty lists to store respective direction's next coordinate 
    choiceDown = []
    choiceUp = [] 
    choiceLeft = [] 
    choiceRight = [] 
    
    # initialize error values
    errorDown = 100
    errorUp = 100
    errorRight = 100
    errorLeft = 100
    
    # error list, values stored in order (up, down, left, right)
    errorList = []
    
    # if (odd, odd) possible directions are down and right
    if ((xc%2 != 0) and (yc%2 !=0 )):
        # Raise corresponding direction flags
        down = 1 
        right = 1
        
        # Calculate possible next coordinate for respective direction
        while (down == 1):
            # Cannot go further down if y == 0
            if (yc == 0):
                break   # break out of this while loop
                
            # Can go down futher if y is not 0 
            else:
                xD = xc 
                yD = yc -2
            
            # append new coordinate to the corresponding list
            choiceDown.append(xD)
            choiceDown.append(yD)
            
            # Calculate error of this coordinate 
            errorDown = CalculateError(choiceDown, goal)
            
            down = 0    # lower flag to move on to next while loop
        
        while (right == 1):
            # cannot go further right if x == 8
            if (xc == 8):
                break
            # can go further right if x is not 3
            else:
                yR = yc
                xR = xc + 2
            
            # append new coordinate to the corresponding list
            choiceRight.append(xR)
            choiceRight.append(yR)
            
            # Calculate error of this coordinate 
            errorRight = CalculateError(choiceRight, goal)
            # lower flag 
            right = 0
            
        
        # Compare the 2 error values and choose the one with the smaller error
        
        # if errorDown is smaller, append the corresponding coordinate into path
        if (errorDown < errorRight):
            path.append(choiceDown)
            
            if(errorDown == 0):
                print("Down")
                return
            else:
                print("Down")
                
                
        elif (errorDown > errorRight):
            path.append(choiceRight)
            # check if the newly added coordinate is the goal
            if (errorRight == 0):
                print("Right")
                return
            else:
                print("Right")
            
        else:
            path.append(choiceDown)
            print("else, down")
            
    
    
    # (even, even) possible directions are up and left
    elif ((xc%2 == 0) and (yc%2 ==0 )):
        up = 1
        left = 1
    
        while (up == 1):
            # Cannot go further up if y == 8
            if (yc == 8):
                break   # get out of this while loop, nothing to change
            # Can go up further if y is not 3
            else:
                yU = yc+ 2
                xU = xc 
            # append new coordinate to the corresponding list
            choiceUp.append(xU)
            choiceUp.append(yU)
            
            # Calculate error of this coordinate 
            errorUp = CalculateError(choiceUp, goal)
            up = 0  # lower flag
        
        while (left == 1):
            # cannot go further left if x == 0
            if (xc == 0):
                break
            # can go further left if x is not 0
            else:
                xL = xc-2
                yL = yc 
            
            # append new coordinate to the corresponding list
            choiceLeft.append(xL)
            choiceLeft.append(yL)
            
            # Calculate error of this coordinate 
            errorLeft = CalculateError(choiceLeft, goal)
            left = 0
    
        # Compare the 2 error values and choose the one with the smaller error
    
        # if errorUp is smaller, append the corresponding coordinate into path
        if (errorUp < errorLeft):
            path.append(choiceUp)
            if (errorUp == 0):
                print("up")
                return
            else:
                print("up")
        elif (errorUp > errorLeft):
            path.append(choiceLeft)
            if (errorLeft == 0):
                print("left")
                return
            else:
                print("left")
        else:   # if 2 errors are equal
            path.append(choiceUp)
            print("else, up")
            
    
    
    # (odd, even) possible directions are down and left
    elif ((xc%2 != 0) and (yc%2 ==0 )):
        down = 1
        left = 1
        
        while (down == 1):
            # cannot go further down if y == 0
            if (yc == 0):
                break
            else:
                yD = yc-2
                xD = xc
            
            # append new coordinate to the corresponding list
            choiceDown.append(xD)
            choiceDown.append(yD)
            
            # Calculate error of this coordinate 
            errorDown = CalculateError(choiceDown, goal)
            down = 0
        
        while (left == 1):
            # cannot go further left if x == 0
            if (xc == 0):
                break
            else:
                xL = xc- 2
                yL = yc
            
            # append new coordinate to the corresponding list
            choiceLeft.append(xL)
            choiceLeft.append(yL)
            
            # Calculate error of this coordinate 
            errorLeft = CalculateError(choiceLeft, goal)
            left = 0
            
        # Compare the 2 error values and choose the one with the smaller error
    
        # if errorUp is smaller, append the corresponding coordinate into path
        if (errorDown < errorLeft):
            path.append(choiceDown)
            if (errorDown == 0):
                print("down")
                return 
            else:
                print("down")
        elif (errorDown > errorLeft):
            path.append(choiceLeft)
            if (errorLeft == 0):
                print("left")
                return
            else:
                print("left")
        else:   # if 2 errors are equal
            path.append(choiceDown)
            
        
        
    # (even, odd) possible directions are up and right
    else:
        # raise direction flags 
        up = 1 
        right = 1 
        
        while (up == 1):
            # Cannot go further up if y == 8
            if (yc == 8):
                break   # get out of this while loop, nothing to change
            # Can go up further if y is not 3
            else:
                yU = yc+2
                xU = xc
            
            # append new coordinate to the corresponding list
            choiceUp.append(xU)
            choiceUp.append(yU)
            
            # Calculate error of this coordinate 
            errorUp = CalculateError(choiceUp, goal)
            up = 0  # lower flag
        
        while (right == 1):
            # cannot go further right if x == 8
            if (xc == 8):
                break
            # can go further right if x is not 3
            else:
                xR = xc+2
                yR = yc
            
            # append new coordinate to the corresponding list
            choiceRight.append(xR)
            choiceRight.append(yR)
            
            # Calculate error of this coordinate 
            errorRight = CalculateError(choiceRight, goal)
            # lower flag 
            right = 0
        
        # Compare the 2 error values and choose the one with the smaller error
    
        # if errorUp is smaller, append the corresponding coordinate into path
        if (errorUp < errorRight):
            path.append(choiceUp)
            if (errorUp == 0):
                print("up")
                return 
            else:
                print("up")
        elif (errorUp > errorRight):
            path.append(choiceRight)
            if (errorRight == 0):
                print("right")
                return 
            else:
                print("right")
        else:   # if 2 errors are equal
            path.append(choiceUp)
            print("else, up")
        
        # By this point, the list path is completed
        
    return     
            

# This function drives the car through all coordinates in path
def Mobilize(dummyStart):
    global path
    global power 
    
    # read initial coordinates 
    xStart = dummyStart[0]
    yStart = dummyStart[1]
    
    # Initialize current x and y 
    xCurr = dummyStart[0]
    yCurr = dummyStart[1]
    
    
    # list of direction indicating where the car is facing
    # in order: up, down, left, right
    direction = [0,0,0,0]
    
    # inidicate the car's orientation originally (what direction the car is facing)
    if (yStart%2==0):    # starting on even row
        if (xStart%2 ==0):  # (even, even) -- turn on upward signal
            direction[0] = 1   
        else:   # (even, odd) -- turn on right signal
            direction[3] = 1
        
    else:   # starting on odd row
        if (xStart%2 ==0):  # (odd, even) -- turn on left signal
            direction[2] = 1    
        else:   # (odd, odd) -- turn on down signal
            direction[1] = 1
    
    
    # getting the car from one point to another by going thru
    # every point in the path list 
    
    i = 0
    j = i+1
    while j < len(path):
        
        x1 = path[i][0]
        x2 = path[j][0]
        y1 = path[i][1]
        y2 = path[j][1]
        
        xdiff = abs(x2 - x1)
        ydiff = abs(y2 - y1)
        
        # check the orientation 
        if (x2 < x1):   # want to go left...
            # check orientation 
            if (direction[0] == 1): # facing up -- turn left first 
                turn_left()
                car.forward(power)
                time.sleep(xdiff/2) # new grid
            
            elif (direction[1] == 1): # facing down -- turn right first 
                turn_right()
                car.forward(power)
                time.sleep(xdiff/2)
            
            elif (direction[2] == 1): # facing left -- go forward 
                car.forward(power)
                time.sleep(xdiff/2)
                
            else:   # facing right, error 
                print("Error")
                
            # update new orientation 
            direction[0] = 0
            direction[1] = 0
            direction[2] = 1
            direction[3] = 0
                
            
        elif (x2 > x1): # want to go right....
            # check orientation 
            if (direction[0] == 1): # facing up -- turn right first 
                turn_right()
                car.forward(power)
                time.sleep(xdiff/2)
            
            elif (direction[1] == 1): # facing down -- turn left first 
                turn_left()
                car.forward(power)
                time.sleep(xdiff/2)
            
            elif (direction[2] == 1): # facing left -- error
                print("Error")
                
            else:   # facing right, go forward 
                car.forward(power)
                time.sleep(xdiff/2)
                
            # update new orientation 
            direction[0] = 0
            direction[1] = 0
            direction[2] = 0
            direction[3] = 1
        
        else:   # when x2 == x1, go either up or down... 
            if (y2 > y1):   # want to go up...
                # check orientation 
                if (direction[0] == 1): # facing up -- go forward
                    car.forward(power)
                    time.sleep(ydiff/2)
                
                elif (direction[1] == 1): # facing down -- error
                    print("Error")
                
                elif (direction[2] == 1): # facing left -- turn right
                    turn_right()
                    car.forward(power)
                    time.sleep(ydiff/2)
                    
                else:               # facing right -- turn left 
                    turn_left()
                    car.forward(power)
                    time.sleep(ydiff/2)
                    
                # update new orientation 
                direction[0] = 1
                direction[1] = 0
                direction[2] = 0
                direction[3] = 0
                
                
            elif (y2 < y1): # want to go down...
                # check orientation 
                if (direction[0] == 1): # facing up -- error
                    print("Error")
                
                elif (direction[1] == 1): # facing down -- go forward
                    car.forward(power)
                    time.sleep(ydiff/2)
                
                elif (direction[2] == 1): # facing left -- turn left
                    turn_left()
                    car.forward(power)
                    time.sleep(ydiff/2)
                    
                else:               # facing right -- turn right 
                    turn_right()
                    car.forward(power)
                    time.sleep(ydiff/2)
                    
                # update new orientation 
                direction[0] = 0
                direction[1] = 1
                direction[2] = 0
                direction[3] = 0
            
            
            else:   
                print("Done")
        
        
        
        
        
        i += 1
        j += 1
   
   
    # End of Mobilize function    
    return
   

def main():
    
    global path
    global power

    
    # reading start and end coordinates 
    initial = get_initial_coord()
    dummyStart = initial
    final = get_final_coord()
    
    # path returns a list of coordinates that the car needs to go thru 
    # to get to its destination
    GetPath(initial, final)
    
    # RECURSION
    while (CalculateError(path[-1], final) != 0):
        initial = path[-1]
        GetPath(initial,final)
    
    # TEST PRINTING
    print("Path list:")
    for i in range(len(path)):
        for j in range(len(path[i])):
            print(path[i][j], end = " ")
        print()
    
    
    # The list path should have all items by this point, 
    # From here, the list will be sorted to only have the main coordinates,
    # This prevents the car from stop-and-go while moving in a straight line
    
    
    path.insert(0, dummyStart)
    # TEST PRINTING
    print("Path list after insertion:")
    for i in range(len(path)):
        for j in range(len(path[i])):
            print(path[i][j], end = " ")
        print()
    
    # After knowing where to go, mobilize through all the coordinates in path
    
    Mobilize(dummyStart)
    car.forward(0)
    

car = Picarx()
main()
    
