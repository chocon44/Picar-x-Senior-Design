
import pico_4wd as car
import time
import math 
import numpy as np
import heapq
from typing import List, Tuple
import pyrebase

# --------- Global parameters ------------#

speed = 50
straightTime = 1
rightSpeed = 50
rightTurnTime = 1.2
leftSpeed = 50 
leftTurnTime = 1.2

#-------- Firebase -----------#

config = {
    'apiKey': "AIzaSyBL9UezOELm7LsBLvfZdlJDkhCTZQAKlx4",
      'authDomain': "jetbot-ece-493.firebaseapp.com",
      'projectId': "jetbot-ece-493",
      'storageBucket': "jetbot-ece-493.appspot.com",
      'messagingSenderId': "906874678062",
      'appId': "1:906874678062:web:6c50c28e26fbb59c0ca8bf",
      'databaseURL': "https://jetbot-ece-493-default-rtdb.firebaseio.com/"
    }

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
database = firebase.database()


class Node:
    def __init__(self, position: Tuple[int, int], g: int = 0, h: int = 0, parent: 'Node' = None):
        self.position = position  # Current position on the grid
        self.g = g  # Cost from start to current node
        self.h = h  # Heuristic cost from current node to end
        self.f = g + h  # Total estimated cost
        self.parent = parent  # Parent node

    def __lt__(self, other):
        # Comparison method for heap queue, based on f value
        return self.f < other.f

def heuristic(a: np.ndarray, b: np.ndarray) -> float:
    a = a.astype(float)
    b = b.astype(float)
    # Calculate Manhattan distance between two points
    return np.abs(a[0] - b[0]) + np.abs(a[1] - b[1])

def get_neighbors(position: np.ndarray, grid: np.ndarray) -> List[np.ndarray]:
    # Generate all possible neighbors (up, down, left, right)
    neighbors = [
        position + [-1, 0],  # Up
        position + [1, 0],   # Down
        position + [0, -1],  # Left
        position + [0, 1]    # Right
    ]
    
    valid_neighbors = []
    
    for i, neighbor in enumerate(neighbors):
        x, y = neighbor
        
        # Check if the neighbor is within grid bounds
        if 0 <= x < grid.shape[0] and 0 <= y < grid.shape[1]:
            # Apply the greenwave movement rules
            if i == 0 and position[1] in [4, 14]:  # Up
                valid_neighbors.append(neighbor)
            elif i == 1 and position[1] in [9, 19]:  # Down
                valid_neighbors.append(neighbor)
            elif i == 2 and position[0] in [9, 19]:  # Left
                valid_neighbors.append(neighbor)
            elif i == 3 and position[0] in [4, 14]:  # Right
                valid_neighbors.append(neighbor)
    
    return valid_neighbors

# This function appends the next found node to path
def reconstruct_path(node: Node) -> List[Tuple[int, int]]:
    # Reconstruct the path from end to start
    path = []
    current = node
    while current:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Reverse to get path from start to end


# This function returns the shortest path from start to end point
def astar(start: np.ndarray, end: np.ndarray, grid: np.ndarray) -> List[Tuple[int, int]]:
    start = start.astype(int)
    end = end.astype(int)
    
    start_node = Node(tuple(start), h=heuristic(start, end))
    open_list = [start_node]  # Priority queue of nodes to be evaluated
    closed_set = set()  # Set of nodes already evaluated

    while open_list:
        current_node = heapq.heappop(open_list)  # Get node with lowest f cost

        if np.array_equal(current_node.position, end):
            return reconstruct_path(current_node)  # Path found

        closed_set.add(current_node.position)

        for neighbor_pos in get_neighbors(np.array(current_node.position), grid):
            if tuple(neighbor_pos) in closed_set:
                continue  # Skip already evaluated neighbors

            neighbor = Node(tuple(neighbor_pos), 
                            g=current_node.g + 1,  # Assume cost of 1 to move to neighbor
                            h=heuristic(neighbor_pos, end),
                            parent=current_node)

            if neighbor not in open_list:
                heapq.heappush(open_list, neighbor)
            else:
                # Update existing neighbor if this path is better
                idx = open_list.index(neighbor)
                if open_list[idx].g > neighbor.g:
                    open_list[idx] = neighbor
                    heapq.heapify(open_list)

    return []  # No path found


# This function shows representation path on grid 
def visualize_path_text(grid_size: int, path: List[Tuple[int, int]]) -> str:
    # Create a text-based visualization of the path
    grid = [['.'] * grid_size for _ in range(grid_size)]
    for x, y in path:
        grid[x][y] = '*'
    grid[path[0][0]][path[0][1]] = 'S'  # Start
    grid[path[-1][0]][path[-1][1]] = 'E'  # End
    return '\n'.join(''.join(row) for row in grid)



        
# 2D list contains coordinates of intersections where there are traffic signals       
intersections =[[4,4],[4,9],[4,14],[4,19],[9,4],[9,9],[9,14],[9,19],
         [14,4],[14,9],[14,14],[14,19],[19,4],[19,9],[19,14],[19,19]]

# This function resets the servo to -10 degree, which is in the middle 
def ServoReset():
    car.servo.set_angle(-10)

# Sweep ultrasonic sensor left and right before making a turn 
# Positive angle is toward the left 
# Negative angle is toward the right 
danger = 15
def ObstacleSweep():
    global danger
    for angle in range(-10, 60): 
        car.servo.set_angle(angle)
        distance = car.sonar.get_distance()
        if (distance < danger):     # if obstacle is detected closely, stop the car
            car.move("stop")
            time.sleep(1)           # stop for 1 sec
            dangerAngle = angle     # note the obstacle detected at this specific angle 
            print("Obstacle is detected at", dangerAngle")
            ObstacleSweep()         # Repeat this function again to check for obstacle 
        time.sleep(0.005)           
    for angle in range(60, -60, -1):
        car.servo.set_angle(angle)
        distance = car.sonar.get_distance()
        if (distance < danger):     # if obstacle is detected closely, stop the car
            car.move("stop")
            time.sleep(1)           # stop for 1 sec
            dangerAngle = angle     # note the obstacle detected at this specific angle 
            print("Obstacle is detected at", dangerAngle")
            ObstacleSweep()         # Repeat this function again to check for obstacle 
        time.sleep(0.005) 
    for angle in range(-60, -10):
        car.servo.set_angle(angle)
        if (distance < danger):     # if obstacle is detected closely, stop the car
            car.move("stop")
            time.sleep(1)           # stop for 1 sec
            dangerAngle = angle     # note the obstacle detected at this specific angle 
            print("Obstacle is detected at", dangerAngle")
            ObstacleSweep()         # Repeat this function again to check for obstacle 
        time.sleep(0.005)


# Check for obstacle in front of car 
def ObstacleAhead():
    global danger 
    ServoReset()            # Reset sensor to face up front 
    if (distance < danger):     # if obstacle is detected closely, stop the car
        car.move("stop")
        time.sleep(1)           # stop for 1 sec
        dangerAngle = angle     # note the obstacle detected at this specific angle 
        print("Obstacle is detected ahead")



up = down = left = right = 0
path = [] 
def Travel(thisPos, nextPos, i):
    global path 
    global up, down, left, right 
    global intersections 
    global speed, rightSpeed, leftSpeed
    global rightTurnTime, leftTurnTime, straightTime
    
    ServoReset() 
    
    # This function checks the Picam pico on firebase
    def RedLight():
        red = database.child("Picam pico").child("Red light detected").get()
        if (red.val() == 1):    # red light is detected 
            car.move("stop")    # stop the car 
            time.sleep(1)       # wait for 1 sec and check again 
            print("Red light ahead")
            RedLight()   
        else:
            print("No red light detected ahead")
            return
        
    if (thisPos == nextPos) :    # when destination is reached, stop the car, stop recursion
        car.stop()
        print("Reached destination")
        return
    
    else:
        thisX = thisPos[0]
        thisY = thisPos[1]
        nextX = nextPos[0]
        nextY = nextPos[1]
        
        # if the next position is an intersection, check for traffic signal
        if (nextPos in intersections):
            RedLight()
        
        
        #--------------- MOVING THE CAR --------------#
        
        if (thisX == nextX):    # on the same horizontal line (row)
            if (thisY < nextY): # go right
                print("Going right")
                
                if (up == 1):
                    ObstacleSweep() # check for obstacle before moving
                    print("- Pivot right")
                    car.move("right", speed)
                    time.sleep(rightTurnTime)
                    car.move("stop")
                    ObstacleAhead()
                    print("- Go forward")
                    car.move("forward", speed)
                    time.sleep(straightTime)
                    car.move("stop")
                    
                    UpdateFirebase(nextX, nextY)    # update current position to firebase 
                    right = 1                   # update current orientation of the car 
                    up = down = left = 0
                
                elif (down == 1):
                    ObstacleSweep() # check for obstacle before moving
                    print("- Pivot left")
                    car.move("left", speed)
                    time.sleep(leftTurnTime)
                    car.move("stop")
                    ObstacleAhead() # check for obstacle before going forward
                    print("- Go forward")
                    car.move("forward", speed)
                    time.sleep(straightTime)
                    car.move("stop")
                    
                    UpdateFirebase(nextX,nextY) # update position to firebase
                    right = 1   # update orientation
                    up = down = left = 0
                
                elif (left == 1):
                    print("Error: facing left going right")
                
                elif (right == 1):
                    ObstacleAhead() # check for obstacle before going forward
                    print("- Go forward")
                    car.move("forward", speed)
                    time.sleep(straightTime)
                    car.move("stop")
                    
                    UpdateFirebase(nextX,nextY) # update position to firebase
                    right = 1   # update orientation
                    up = down = left = 0
                
            else: # go left     
                print("Going left")
                if (up == 1):
                    ObstacleSweep() 
                    print("- Pivot left")
                    car.move("left", speed)
                    time.sleep(leftTurnTime)
                    car.move("stop")
                    ObstacleAhead() # check for obstacle before going forward
                    print("- Go forward")
                    car.move("forward", speed)
                    time.sleep(straightTime)
                    car.move("stop")
                    UpdateFirebase(nextX,nextY) # update position to firebase
                    left = 1   # update orientation
                    up = down = right = 0
                    
                elif (down == 1):
                    ObstacleSweep() # check for obstacle before moving
                    print("- Pivot right")
                    car.move("right", speed)
                    time.sleep(rightTurnTime)
                    car.move("stop")
                    ObstacleAhead()
                    print("- Go forward")
                    car.move("forward", speed)
                    time.sleep(straightTime)
                    car.move("stop")
                    UpdateFirebase(nextX,nextY) # update position to firebase
                    left = 1   # update orientation
                    up = down = right = 0
                    
                elif (left == 1):
                    ObstacleAhead() # check for obstacle before going forward
                    print("- Go forward")
                    car.move("forward", speed)
                    time.sleep(straightTime)
                    car.move("stop")
                    UpdateFirebase(nextX,nextY) # update position to firebase
                    left = 1   # update orientation
                    up = down = right = 0
                    
                elif (right == 1):
                    print("Error: facing right going left")
                    
        elif (thisY == nextY):    # on the same vertical line (column)
            if (thisX > nextX): # go up
                print("Going up")
                if (up == 1):
                    ObstacleAhead() # check for obstacle before going forward
                    print("- Go forward")
                    car.move("forward", speed)
                    time.sleep(straightTime)
                    car.move("stop")
                    UpdateFirebase(nextX,nextY) # update position to firebase
                    up = 1   # update orientation
                    left = down = right = 0
                
                elif (down == 1):
                    print("Error: facing down going up")
                elif (left == 1):
                    ObstacleSweep() # check for obstacle before moving
                    print("- Pivot right")
                    car.move("right", speed)
                    time.sleep(rightTurnTime)
                    car.move("stop")
                    ObstacleAhead()
                    print("- Go forward")
                    car.move("forward", speed)
                    time.sleep(straightTime)
                    car.move("stop")
                    UpdateFirebase(nextX,nextY) # update position to firebase
                    up = 1   # update orientation
                    left = down = right = 0
                elif (right == 1):
                    ObstacleSweep() # check for obstacle before moving
                    print("- Pivot left")
                    car.move("left", speed)
                    time.sleep(leftTurnTime)
                    car.move("stop")
                    ObstacleAhead() # check for obstacle before going forward
                    print("- Go forward")
                    car.move("forward", speed)
                    time.sleep(straightTime)
                    car.move("stop")
                    UpdateFirebase(nextX,nextY) # update position to firebase
                    up = 1   # update orientation
                    left = down = right = 0
            
            else:   # go down
                print("Going down")
                if (up == 1):
                    print("Error: facing up going down")
                elif (down == 1):
                    ObstacleAhead() # check for obstacle before going forward
                    print("- Go forward")
                    car.move("forward", speed)
                    time.sleep(straightTime)
                    car.move("stop")
                    UpdateFirebase(nextX,nextY) # update position to firebase
                    down = 1   # update orientation
                    left = up = right = 0
                elif (left == 1):
                    ObstacleSweep() # check for obstacle before moving
                    print("- Pivot left")
                    car.move("left", speed)
                    time.sleep(leftTurnTime)
                    car.move("stop")
                    ObstacleAhead() # check for obstacle before going forward
                    print("- Go forward")
                    car.move("forward", speed)
                    time.sleep(straightTime)
                    car.move("stop")
                    UpdateFirebase(nextX,nextY) # update position to firebase
                    down = 1   # update orientation
                    left = up = right = 0
                 elif (right == 1):
                    ObstacleSweep() # check for obstacle before moving
                    print("- Pivot right")
                    car.move("right", speed)
                    time.sleep(rightTurnTime)
                    car.move("stop")
                    ObstacleAhead()
                    print("- Go forward")
                    car.move("forward", speed)
                    time.sleep(straightTime)
                    car.move("stop")
                    UpdateFirebase(nextX,nextY) # update position to firebase
                    down = 1   # update orientation
                    left = up = right = 0
        
        # Increment and recursively repeat this function until destination is reached
        i+=1        # increment i
        if (i+1 >= len(path)):
            print("Done")
            car.move("stop")
            return
        else:
            thisPos = path[i]
            nextPos = path[i+1]
            Travel(thisPos,nextPos,i)     # recursion
            car.move("stop")
    
    
    
    
def UpdateFirebase(x,y):
    data = {
    "Current row": x,      
    "Current column": y}
    
    database.child("Pico 4wd").child("Current position").set(data)
    car.move("stop")


# Determines position, convert path list, initialize parameters for Travel() function 
def Mobilize(starting, ending, path_list):
    global up, down, left, right
    global path
    
    for coord in path_list:
        # Convert tuple coordinates to list of integers
        path.append([int(coord[0]), int(coord[1])])
    if not path:
        print("Empty path provided")
        return
    
    start = path[0]
    
    down_list = [4,19]      #[[0,9], [0,19], [4,19], [9,19], [14,19]]
    up_list = [4,14]       #[[19,4], [19,14]]
    left_list = [9,19]      #[[19,19], [19,9]] 
    right_list = [4,14]     #[[4,0], [14,0]]
    
    # Initial orientation
    if (start[0] in right_list):
        right = 1
        print("Original orientation: right")
    elif (start[0] in left_list):
        left = 1
        print("Original orientation: left")
    elif (start[1] in up_list):
        up = 1
        print("Original orientation: up")
    elif (start[1] in down_list):
        down = 1
        print("Original orientation: down")
    
    #-----  Moving the car from here to end of function -------# 
    i = 0
    curr = path[i] 
    nxt = path[i+1]
    Travel(curr, nxt ,i)
    car.stop()
    return



def UpdateFirebase(x,y):
    data = {
    "Current row": x,      
    "Current column": y}
    
    database.child("Pico 4wd").child("Current position").set(data)
    car.stop()

def GetInitials():      # just added 
    x1 = input("Enter starting x value: ")
    y1 = input("Enter starting y value: ")
    return([x1,y1])

def GetEnding():
    x2 = input("Enter ending x value: ")
    y2 = input("Enter ending y value: ")
    return([x2,y2])

def main():
    grid_size = 20
    grid = np.zeros((grid_size, grid_size))  # Create an empty grid
    
    start = np.array(GetInitials())  
    end = np.array(GetEnding())  
    
    path = astar(start, end, grid)
    
    if path:
        print("Shortest path found:")
        for x, y in path:
            print(f"({x}, {y})", end=" -> ")
        print("Done")
        print("\nText representation of the path:")
        print(visualize_path_text(grid_size, path))
    else:
        print("No path found.")
    
    #------ Pushing to firebase ---------#
    
    data = {
    "Starting x coordinate": start[0],      
    "Starting y coordinate": start[1],
    "Ending x coordinate": end[0],
    "Ending y coordinate" : end[1]}
    
    database.child("Pico 4wd").child("Coordinates").set(data)
    
    ServoReset()
    
    Mobilize(start,end,path)    # drive the car to destination
    car.stop()
    
    ServoReset()
    
    
    

if __name__ == "__main__":
    main()
    car.move("stop")
    ServoReset()
