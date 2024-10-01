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
# Moving in X and Y directions using xdiff and ydiff
# Last updated: 9/30


from picarx import Picarx 
import math 
import time
import numpy as np
import heapq
from typing import List, Tuple
import pyrebase



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




#-------- Initialization -----------#

car = Picarx()
leftTurnTime = 1    # time to pivot turn the car left 90 degrees
rightTurnTime = 1.5   # time to pivot turn the car right 90 degrees
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


# This function checks the car's orientation and move the car 
def Mobilize(starting, ending, path_list):
    # This function drives the Picarx
    global leftTurnTime
    global rightTurnTime
    global t
    global turnPower
    global power 
    
    start = []
    # new 2d list to store all coordinates
    size = int(len(path_list)/2)
    path = [[] for i in range(size)]
    # copy all nodes in path_list to path as sub lists 
    i = 0
    dummy = 0
    while (i+1 < len(path_list)):
        path[dummy].append(path_list[i])
        path[dummy].append(path_list[i+1])
        i+=2
        dummy+=1

    # store initial coordinates 
    start = [] 
    start.append(path[0][0])
    start.append(path[0][1])
    # store ending coordinates
    end = []
    end.append(path[-1][0])
    end.append(path[-1][1])

    
    
    # list of coordinates that have named original orientation 
    down_list = [[0,9], [0,19], [4,19], [9,19], [14,19]]
    up_list = [[19,4], [19,14]]
    left_list = [[19,19], [19,9]] 
    right_list = [[4,0], [14,0]]
    
    # flags to indicate orientation 
    up = 0
    down = 0
    left = 0
    right = 0

    # Check orientation of the car originally 
   
    if (start in down_list):
        up = 0
        down = 1
        left = 0
        right = 0
    elif (start in up_list):
        up = 1
        down = 0
        left = 0
        right = 0
    elif (start in left_list):
        up = 0
        down = 0
        left = 1
        right = 0
    elif (start in right_list):
        up = 0
        down = 0
        left = 0
        right = 1

   #######################################3
    print("First coordinate: ",path_list[0])
    print("x1: ", path_list[0][0])
    print("y1: ",path_list[0][1])
    print("x2: ", path_list[-1][0])
    print("y2: ", path_list[-1][1])

    #-----  Moving the car -------# READ FROM DATABASE
    
    
    i = 0
    j = i+1
    while j < len(path):
        
        startX = path_list[i][0]
        startY = path_list[i][1]
        endX = path[j][0]
        endY = path[j][1]
        
        xdiff = int(abs(endX-startX))
        ydiff = int(abs(endY - startY))

        if (endX < startX).all():     # want to go left ...
        
            # checking orientation 
            if (up == 1):       # facing up, turn left then go forward 
                car.left(turnPower)
                time.sleep(leftTurnTime)
                car.forward(power)
                time.sleep(xdiff)
            elif (down == 1):   # facing down, turn right then go forward
                car.right(power)
                time.sleep(rightTurnTime)
                car.forward(power)
                time.sleep(xdiff)
            elif (left == 1):   # go forward only
                car.forward(power)
                time.sleep(xdiff)
            else:               # facing right, error
                print("Error: Facing right going left")
                car.stop()
            
            # update new orientation to left 
            up = 0
            down = 0
            left = 1
            right = 0
        
        elif (endX > startX).all():   # want to go right ...
            # checking orientation 
            if (up == 1):       # facing up, turn right then go forward 
                car.right(turnPower)
                time.sleep(rightTurnTime)
                car.forward(power)
                time.sleep(xdiff)
            elif (down == 1):   # facing down, turn left then go forward
                car.left(power)
                time.sleep(leftTurnTime)
                car.forward(power)
                time.sleep(xdiff)
            elif (right == 1):   # go forward only
                car.forward(power)
                time.sleep(xdiff)
            else:# left          # facing right, error
                print("Error: Facing left going right")
                car.stop()
            
            # update new orientation to left 
            up = 0
            down = 0
            left = 1
            right = 0
        
        else:       # when endX = startX, go either up or down .... 
        
            if (endY > startY).all():     # want to go up...
                # check orientation 
                if (up == 1):   # just go forward 
                    car.forward(power)
                    time.sleep(ydiff)
                elif (down == 1):   # error 
                    print("Error: Facing down going up")
                elif (left == 1):   # facing left, turn right first 
                    car.right(power)
                    time.sleep(rightTurnTime)
                else:   # facing right, turn left first 
                    car.left(power)
                    time.sleep(leftTurnTime)
                    
                # update new orientation to up 
                up = 1
                down = 0
                left = 0
                right = 0
            
            elif (endY < startY).all():   # want to go down...
                # check orientation 
                if (up == 1):   # facing up, print error 
                    print("Error: Facing up going down")
                
                elif (down == 1):   # go forward 
                    car.forward(power)
                    time.sleep(ydiff)
                    
                elif (left == 1):   # turn left first 
                    car.left(power)
                    time.sleep(leftTurnTime)
                    car.forward(power)
                    time.sleep(ydiff)
                    
                else:           # turn right first 
                    car.right(power)
                    time.sleep(rightTurnTime)
                    car.forward(power)
                    time.sleep(ydiff)
            
            else:
                print("Done")
        i +=1
        j +=1
        return      # end of Mobilize function 
        

# this function returns a value for color of traffic light detected
# def Camera_Vision():
    
    
    
    
    # return light 

def main():
    grid_size = 20
    grid = np.zeros((grid_size, grid_size))  # Create an empty grid
    
    start = np.array([9, 19])  # Starting position
    end = np.array([4, 19])  # Ending position
    
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

        
    
    #------ Sending to firebase ---------#
    
    data = {
    "Starting x coordinate": 9,
    "Starting y coordinate": 19,
    "Ending x coordinate": 4,
    "Ending y coordinate" : 19}
    
    database.child("Picarx4").child("Coordinates").set(data)
    database.child("Picarx4").child("Push data").push(data)
    
    #time.sleep(3)
    
    Mobilize(start,end,path)    # drive the car to destination




if __name__ == "__main__":
    main()
    car.stop()
