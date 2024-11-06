import numpy as np
import time
import pyrebase
import sys

sys.stdout.reconfigure(encoding='utf-8')
# Firebase configuration
firebaseConfig = {
  'apiKey': "AIzaSyBL9UezOELm7LsBLvfZdlJDkhCTZQAKlx4",
  'authDomain': "jetbot-ece-493.firebaseapp.com",
  'projectId': "jetbot-ece-493",
  'storageBucket': "jetbot-ece-493.appspot.com",
  'messagingSenderId': "906874678062",
  'appId': "1:906874678062:web:6c50c28e26fbb59c0ca8bf",
  'databaseURL': "https://jetbot-ece-493-default-rtdb.firebaseio.com/"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
database = firebase.database()


# Create a matrix to represent the grid
grid_size = 20
grid = np.zeros((grid_size, grid_size), dtype=int)

# Define road positions
road_positions = [4, 9, 14, 19]  # Positions of the roads

def create_roads(grid):
    """Create the road layout on the grid."""
    for pos in road_positions:
        grid[pos, :] = 1  # Horizontal roads
        grid[:, pos] = 1  # Vertical roads
    return grid

def update_green_waves(grid, wave_positions):
    """Update the positions of green waves on the roads."""
    for road in [4, 9, 14]:
        grid[:, road] = 1  # Reset vertical roads
    for road in [4, 9, 14]:
        grid[road, :] = 1  # Reset horizontal road
    green_length = 9  # Length of each green wave

    # Update waves on first vertical road (moving up)
    for i in range(green_length):
        pos = (wave_positions[0] - i) % grid_size
        grid[pos, 4] = 2           # 1 green wave
        #pos = (wave_positions[1] - i) % grid_size
        #grid[pos, 4] = 2

    # Update waves on second vertical road (moving down)
    for i in range(green_length):
        pos = (wave_positions[1] + i) % grid_size
        grid[pos, 9] = 2
        #pos = (wave_positions[3] + i) % grid_size
        #grid[pos, 9] = 2

    # Update waves on third vertical road (moving up)
    for i in range(green_length):
        pos = (wave_positions[2] - i) % grid_size
        grid[pos, 14] = 2
        #pos = (wave_positions[5] - i) % grid_size
        #grid[pos, 14] = 2

    # Update waves on horizontal road (moving right)
    for i in range(green_length):
        pos = (wave_positions[3] + i) % grid_size
        grid[4, pos] = 3
        # pos = (wave_positions[7] + i) % grid_size
        # grid[4, pos] = 1

    # Update waves on horizontal road (moving right)
    for i in range(green_length):
        pos = (wave_positions[4] - i) % grid_size
        grid[9, pos] = 3
        # pos = (wave_positions[9] - i) % grid_size
        # grid[9, pos] = 1

    # Update waves on horizontal road (moving right)
    for i in range(green_length):
        pos = (wave_positions[5] + i) % grid_size
        grid[14, pos] = 3
        # pos = (wave_positions[11] + i) % grid_size
        # grid[14, pos] = 1

    return grid

def print_grid(grid):
    """Print a visual representation of the grid."""
    print("Grid status (Green waves on three vertical roads, blue waves on horizontal road):")
    for row in grid:
        line = ''
        for cell in row:
            if cell == 0:
                line += '🟥'  # Red square for non-road
            elif cell == 1:
                line += '🟫'  # Brown square for road
            elif cell == 2:
                line += '🟩'  # Green square for vertical green wave
            elif cell == 3:
                line += '🟦'  # Blue square for horizontal green wave
        print(line.encode('utf-8').decode('utf-8'))
    print("\n" + "=" * 40)

# function to update firebase with current light state
def update_light(wave,state):
    database.child("traffic_light").update({wave: state})

# set current light states
def set_light_states(wave_positions):
    # hoz waves
    if (wave_positions[3] >= 1 and wave_positions[3] <= 5) or (wave_positions[3] >= 11 and wave_positions[3] <= 15):
        update_light("hoz_t","out")
        update_light("hoz_b","out")
        update_light("hoz_m", "in")
    else:
        update_light("hoz_t", "in")
        update_light("hoz_b", "in")
        update_light("hoz_m", "out")

    # vert waves
    if (wave_positions[0] >= 13 and wave_positions[0] <= 17) or (wave_positions[0] >= 3 and wave_positions[0] <= 7):
        update_light("vert_l", "out")
        update_light("vert_r", "out")
        update_light("vert_c", "in")
    else:
        update_light("vert_l", "in")
        update_light("vert_r", "in")
        update_light("vert_c", "out")



def update_firebase(wave_positions):
    """Update Firebase with the current green wave positions."""
    green_wave_data = {
        "vertical_waves": {
            "road_4": {"wave_1": wave_positions[0],  "direction": "up"},
            "road_9": {"wave_1": wave_positions[1], "direction": "down"},
            "road_14": {"wave_1": wave_positions[2],  "direction": "up"}
        },
        "horizontal_waves": {
            "road_4": {"wave_1": wave_positions[3], "direction": "right"},
            "road_9": {"wave_1": wave_positions[4], "direction": "left"},
            "road_14": {"wave_1": wave_positions[5], "direction": "right"}
        }
    }
    database.child("green_waves").set(green_wave_data)

# Initialize the grid with roads
grid = create_roads(grid)

# Initialize wave positions
wave_positions = [
    #grid_size - 2,  # First wave on first vertical road (up)
    3,  # Second wave on first vertical road (up) -- [0]
    0,  # First wave on second vertical road (down)-- [1]
    #0,  # Second wave on second vertical road (down) 
    13,  # First wave on third vertical road (up)-- [2]
    #0 ,  # Second wave on third vertical road (up) 
    
    15,  # First wave on horizontal road (right)-- [3]
    #0,  # Second wave on horizontal road (right) 
    8,  # First wave on horizontal road (left) --[4]
    #0,  # Second wave on horizontal road (left) 
    5,  # First wave on horizontal road (right) --[5]
    #15  # Second wave on horizontal road (right) 
]

# Main loop
while True:
    # Update green waves
    grid = update_green_waves(grid, wave_positions)

    # Print the current grid status
    print_grid(grid)

    # Update Firebase
    update_firebase(wave_positions)
    set_light_states(wave_positions)

    # Move the waves
    wave_positions[0] = (wave_positions[0] - 1) % grid_size  # Move up
    #wave_positions[1] = (wave_positions[1] - 1) % grid_size  # Move up
    wave_positions[1] = (wave_positions[1] + 1) % grid_size  # Move down
    #wave_positions[3] = (wave_positions[3] + 1) % grid_size  # Move down
    wave_positions[2] = (wave_positions[2] - 1) % grid_size  # Move up
    #wave_positions[5] = (wave_positions[5] - 1) % grid_size  # Move up
    wave_positions[3] = (wave_positions[3] + 1) % grid_size  # Move right
    #wave_positions[7] = (wave_positions[7] + 1) % grid_size  # Move right
    wave_positions[4] = (wave_positions[4] - 1) % grid_size  # Move left
    #wave_positions[9] = (wave_positions[9] - 1) % grid_size  # Move left
    wave_positions[5] = (wave_positions[5] + 1) % grid_size  # Move right
    #wave_positions[11] = (wave_positions[11] + 1) % grid_size  # Move right

    # Wait for a short time before the next update
    time.sleep(0.3) #0.57 ~4s current