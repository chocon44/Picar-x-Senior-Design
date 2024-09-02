#-----------------
# CODE FROM MY-EXAMPLE
#
# LAST UPDATED: 9/2/24 
#
# FOR PICO 4WD
# DESCRIPTION: PATH SEARCHING TESTING 
# 
# NOTES: New grid implemented - want obstacle emergency stop - want reroute - want light flash
#-----------------

import pico_4wd as car
import time
from pico_rdp import Motor, Speed, Servo, Ultrasonic, WS2812, mapping
from machine import Pin, ADC, Timer
import math
import time

path = []
power = 40
turningTime = 1     # for 90 degrees

# This function returns the target destination 
# Returns a list of x,y
def get_final_coord():  
#     endx = int(input("Enter destination x coordinate: "))
#     endy = int(input("Enter destination y coordinate: "))
#     end = [endx,endy]
    end = [0,0]
    return end
    
# This function returns the starting position 
# Returns a list of x,y
def get_initial_coord():
#     startx = int(input("Enter starting x coordinate: "))
#     starty = int(input("Enter starting y coordinate: "))
#     start = [startx,starty]
    start = [0,8]
    return start






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
    
    left_ylist = [8,4,0]
    right_ylist = [6,2]
    up_xlist = [2,6]
    down_xlist = [0,4,8]
    
    if xc in up_xlist:
        up = 1
    elif xc in down_xlist:
        down = 1
    if yc in left_ylist:
        left = 1
    elif yc in right_ylist:
        right = 1
    
    # Possible moves are down and right
    if (down == 1) and (right == 1):
        while (down == 1):
            # Cannot go further down is y == 0
            if (yc == 0):
                break
            # if current y is not 0 
            else:
                xD = xc 
                yD = yc-2
            
            # Append new coordinate to corresponding list 
            choiceDown.append(xD)
            choiceDown.append(yD)
            
            # Calculate error of this coordinate 
            errorDown = CalculateError(choiceDown, goal)
            
            # Lower down flag 
            down = 0
            
        while (right == 1):
            # Cannot go further right if x == 8
            if (xc == 8):
                break
            # if the current x is not 8
            else:
                yR = yc
                xR = xc+2
            
            # Append new coordinate to the list 
            choiceRight.append(xR)
            choiceRight.append(yR)
            
            # Calculate error of this coordinate 
            errorRight = CalculateError(choiceRight, goal)
            right = 0
            
        # Compare the 2 error values and choose the smaller one 
        
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
    
    elif (up == 1) and (left == 1):
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
    
    
    elif (down == 1) and (left == 1):
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
    
        # if errorDown is smaller, append the corresponding coordinate into path
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
    
    
    
    else: # (up == 1) and (right == 1):
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
    global turningTime
    
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
            
            # check for obstacle
            
            # check orientation 
            if (direction[0] == 1): # facing up -- turn left first 
                car.move("left", power)
                time.sleep(turningTime)   # turning 90 degrees
                car.move("forward", power)
                time.sleep(xdiff/2) # new grid
            
            elif (direction[1] == 1): # facing down -- turn right first 
                car.move("right", power)
                time.sleep(turningTime)
                car.move("forward",power)
                time.sleep(xdiff/2)
            
            elif (direction[2] == 1): # facing left -- go forward 
                car.move("forward",power)
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
                car.move("right", power)
                time.sleep(turningTime)
                car.move("forward",power)
                time.sleep(xdiff/2)
            
            elif (direction[1] == 1): # facing down -- turn left first 
                car.move("left", power)
                time.sleep(turningTime)
                car.move("forward",power)
                time.sleep(xdiff/2)
            
            elif (direction[2] == 1): # facing left -- error
                print("Error")
                
            else:   # facing right, go forward 
                car.move("forward",power)
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
                    car.move("forward",power)
                    time.sleep(ydiff/2)
                
                elif (direction[1] == 1): # facing down -- error
                    print("Error")
                
                elif (direction[2] == 1): # facing left -- turn right
                    car.move("right", power)
                    time.sleep(turningTime)
                    car.move("forward",power)
                    time.sleep(ydiff/2)
                    
                else:               # facing right -- turn left 
                    car.move("left", power)
                    time.sleep(turningTime)
                    car.move("forward",power)
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
                    car.move("forward",power)
                    time.sleep(ydiff/2)
                
                elif (direction[2] == 1): # facing left -- turn left
                    car.move("left", power)
                    time.sleep(turningTime)
                    car.move("forward",power)
                    time.sleep(ydiff/2)
                    
                else:               # facing right -- turn right 
                    car.move("right", power)
                    time.sleep(turningTime)
                    car.move("forward",power)
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
    car.move("stop")
    



try:
    main()

finally:
    car.move("stop")




