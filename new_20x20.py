# Green wave notes: 

# Can travel: row = 4,9,14,19; column = 4,9,14,19
# Cannot travel: all other row and column
# Direction:
    # - toward smaller col value (arrow up) : col = 4, 14
    # - toward greater col value (arrow down): col = 9, 19
    # - toward smaller row value (arrow left) : row = 9, 19
    # - toward greater row value (arrow right): row = 4,14
    # - Can only start at the following coordinates: 
    #    (0,9), (0,19), (4,0), (14,0), (19,4), (19,9),(19,14),(19,19), (0,19),(4,19),(9,19),(14,19), (19,19)
    # - Intersections at 
    #    [[4,4],[4,9],[4,14],[4,19],[9,4],[9,9],[9,14],[9,19],
    #     [14,4],[14,9],[14,14],[14,19],[19,4],[19,9],[19,14],[19,19]]
    
# Moving in X and Y directions using xdiff and ydiff
# Last updated: 10/12


from picarx import Picarx 
import math 
import time
import numpy as np
import heapq
from typing import List, Tuple
import pyrebase
from vilib import Vilib



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



#------------- Initialize -----------------#


car = Picarx()
leftTurnTime = 1    # time to pivot turn the car left
rightTurnTime = 1.5   # time to pivot turn the car right
turnPower = 50  # power to pivot turn 
power = 50      # power to go forward
t = 1           # time for car going forward, 1 block distance

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
            # Apply the specific movement rules
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



# this function returns 1 if red light is detected, 0 if green light detected 
def RedLight():
    Vilib.camera_start()
    #Vilib.display()        # turn display on when needed
    Vilib.color_detect("red")
    
    if Vilib.detect_obj_parameter['color_n']!=0:    # if red is detected
        car.stop()      # stop the car immediately 
        return 1
    else:   # if red is not detected -- green or yellow
        return 0 
    

        
# 2D list contains coordinates of intersections where there are traffic signals       
intersections =[[4,4],[4,9],[4,14],[4,19],[9,4],[9,9],[9,14],[9,19],
         [14,4],[14,9],[14,14],[14,19],[19,4],[19,9],[19,14],[19,19]]

# This function checks the car's orientation and move the car 
def Mobilize(starting, ending, path_list):
    # This function drives the Picarx
    global leftTurnTime
    global rightTurnTime
    global t
    global turnPower
    global power 
    global intersections 
    
     # new 2d list to store all coordinates
    path = []
    for coord in path_list:
        # Convert tuple coordinates to list of integers
        path.append([int(coord[0]), int(coord[1])])
    
    if not path:
        print("Empty path provided")
        return
        
    start = path[0]
    end = path[-1]
    
    # Initialize current position tracker
    current_x = start[0]
    current_y = start[1]
    
    
    # ---------- Function to update Firebase with current position -----------#
    
    def update_position(x, y):
        data = {
            "Current x": int(x),
            "Current y": int(y)
        }
        database.child("Picarx4").child("Current location").set(data)
        print(f"Position updated: ({x}, {y})")
    
    
    #------------ Function to interpolate positions during movement -----------#
    
    def move_with_updates(start_pos, end_pos, movement_time):
        steps = 10  # Number of position updates during movement
        x_start, y_start = start_pos
        x_end, y_end = end_pos
        
        for i in range(steps + 1):
            # Calculate intermediate position
            progress = i / steps
            current_x = x_start + (x_end - x_start) * progress
            current_y = y_start + (y_end - y_start) * progress
            
            # Update Firebase with current position
            update_position(current_x, current_y)
            
            # Wait for a fraction of the movement time
            time.sleep(movement_time / steps)
    
    
   
    def update_location(currentx, currenty):
        
        
        data = {
        "Current x coordinate" : currentx,
        "Current y coordinate" : currenty}
        database.child("Picarx4").child("Current location").set(data)
        time.sleep(1)
    
    
    
    
    #------- list of coordinates that have named original orientation ------# 
    
    down_list = [[0,9], [0,19], [4,19], [9,19], [14,19]]
    up_list = [[19,4], [19,14]]
    left_list = [[19,19], [19,9]] 
    right_list = [[4,0], [14,0]]
    
    
    
    # flags to indicate orientation 
    up = down = left = right = 0
    
    # Set initial orientation
    if start in down_list: 
        down = 1
        print("Original orientation: down")
    elif start in up_list: 
        up = 1
        print("Original orientation: up")
    elif start in left_list: 
        left = 1
        print("Original orientation: left")
    elif start in right_list: 
        right = 1
        print("Original orientation: right")
    
    
    
    
    #-----  Moving the car from here to end of function -------# READ FROM DATABASE
    
    
    i = 0
    j = i+1
    while j < len(path):
    
    
        # this is the current location of the car 
        startX = path[i][0]
        startY = path[i][1]
        
        # This represent the next coordinate the car is traveling to
        nextX = path[j][0]
        nextY = path[j][1]
        nextPos = [nextX, nextY]
        
        
        xdiff = abs(nextX - startX)      # difference between current and the next x value
        ydiff = abs(nextY - startY)      # difference between current and the next y value
        
        
        
        #----------- Traffic signal check ----------------#
        
        # if (nextPos in intersections):  # if car is approaching intersection 
            # if (RedLight() == 0):   # if no red light is detected... continue on 
                # print("No red light detected")
                # break;
            # else:          #  Red light is detected, continue this loop until light is green
                # while (RedLight() != 0):
                    # print("Stop at red light")
                    # car.stop()
                    # time.sleep(1)
            
            
            
       #----------- Check for obstacle in front of the car ----------- #
        
        
        
        
        #----------- Movement logic ----------- #
        

        if (nextX < startX):     # want to go up ...
            print("Going up...")
            time.sleep(1)
            # checking orientation 
            if (up == 1):       # go forward 
                
                print("- Go forward")
                time.sleep(1)
                car.forward(power)
                time.sleep(xdiff)
                
            elif (down == 1):   # error
                print("Error: facing down going up")
                car.stop()
                
                
            elif (left == 1):   # 
                print("- Pivot right")
                time.right(turnPower)
                time.sleep(rightTurnTime)
                
                print("- Go forward")
                time.sleep(1)
                car.forward(power)
                time.sleep(xdiff)
                
            else:               # 
                print("- Pivot left")
                time.left(turnPower)
                time.sleep(leftTurnTime)
                print("- Go forward")
                time.sleep(1)
                car.forward(power)
                time.sleep(xdiff)
            

            
            # update new orientation to left 
            print("Car is facing up")
            down = left = right= 0
            up = 1
        
        
        
        elif (nextX > startX):   # want to go down ...
            print("Going down...")
            time.sleep(1)
            
            # checking orientation 
            if (up == 1):     
                print("Error: Facing up going down")
                car.stop()
                
                
                
            elif (down == 1):   #
                
                print("- Go forward")
                time.sleep(1)
                car.forward(power)
                time.sleep(xdiff)
                
            elif (right == 1):   # go down then forward 
                print("- Pivot right")
                time.right(turnPower)
                time.sleep(rightTurnTime)
                print("- Go forward")
                time.sleep(1)
                car.forward(power)
                time.sleep(xdiff)
                
                
                
            else:# left          # 
                print("- Pivot left")
                time.left(turnPower)
                time.sleep(leftTurnTime)
                print("- Go forward")
                time.sleep(1)
                car.forward(power)
                time.sleep(xdiff)
            
           
            
            # update new orientation to left 
            print("Car facing down")
            up = left = right= 0
            down = 1
            

        else:       # when nextX = startX, go either left or right .... 
        
            if (nextY > startY):     # want to go right...
                print("Going right...")
                time.sleep(1)
                
                # check orientation 
                if (up == 1):   # turn right first
                    print("- Pivot right")
                    time.right(turnPower)
                    time.sleep(rightTurnTime)
                    print("- Go forward")
                    time.sleep(1)
                    car.forward(power)
                    time.sleep(ydiff)
                    
                    
                elif (down == 1):   # turn left first
                    print("- Pivot left")
                    time.sleep(1)
                    car.right(power)
                    time.sleep(rightTurnTime)
                    print("- Go forward")
                    time.sleep(1)
                    car.forward(power)
                    time.sleep(ydiff)
                    
                    
                elif (left == 1):   # facing left, turn right first 
                    print("Error: left going right")
                    car.stop()
                    
                else:   # facing right, forward only
                    print("- Go forward")
                    time.sleep(1)
                    car.forward(power)
                    time.sleep(ydiff)
                    
               
                
                # update new orientation to up 
                print("Car facing right")
                right = 1
                down = left= up = 0
            

            elif (nextY < startY):   # want to go left...
                print("Going left...")
                time.sleep(1)
                
                # check orientation 
                if (up == 1):   # turn left fist then forward
                    print("- Pivot left")
                    time.sleep(1)
                    car.left(power)
                    time.sleep(leftTurnTime)
                    
                    print("- Go forward")
                    time.sleep(1)
                    car.forward(power)
                    time.sleep(ydiff)
                   
                
                elif (down == 1):   # turn right first then forward
                    print("- Pivot RIGHT")
                    time.sleep(1)
                    car.right(power)
                    time.sleep(rightTurnTime)
                    
                    print("- Go forward")
                    time.sleep(1)
                    car.forward(power)
                    time.sleep(ydiff)
                    
                    
                elif (left == 1):   # forward only
                    print("- Go forward")
                    time.sleep(1)
                    car.forward(power)
                    time.sleep(ydiff)
                   
                    
                else:           # error
                    print("Error: facing right going left")
                    car.stop()
                
                # update new orientation to left
                print("Car facing left")
                left = 1
                down = right= up = 0
            
            else:
                print("Done")
                
        
        
        print("i = ", i)
        print("j = ", j )
        i +=1
        j +=1
        return      # end of Mobilize function 
        
    
        
    
    
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
    
    # start = np.array([9, 19])  # Starting position
    # end = np.array([4, 19])  # Ending position
    
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
    "Starting x coordinate": start[0],      # syntax error here due to coordinates
    "Starting y coordinate": start[1],
    "Ending x coordinate": end[0],
    "Ending y coordinate" : end[1]}
    
    database.child("Picarx4").child("Coordinates").set(data)
    #database.child("Picarx4").child("Coordinates").push(data)   # Try this instead of set 
    
    
    #time.sleep(3)    # try turning this on and off to see the difference
    
    Mobilize(start,end,path)    # drive the car to destination




if __name__ == "__main__":
    main()
    car.stop()
