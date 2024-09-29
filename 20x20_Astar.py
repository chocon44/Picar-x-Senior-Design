# Green wave notes: 

# Can travel: row = 4,9,14,19; column = 4,9,14,19
# Cannot travel: all other row and column
# Direction:
    # - toward smaller col value (arrow up) : col = 4, 14
    # - toward greater col value (arrow down): col = 9, 14
    # - toward smaller row value (arrow left) : row = 9, 19
    # - toward greater row value (arrow right): row = 4,14
    # - Can only start at the following coordinates: 
    #    (0,9), (0,19), (4,0), (14,0), (19,4), (19,9),(19,14),(19,19), (0,19),(4,19),(9,19),(14,19), (19,19)




import numpy as np
import heapq
from typing import List, Tuple

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
        position + [0, 1], position + [0, -1],
        position + [1, 0], position + [-1, 0]
    ]
    # Filter valid neighbors: within grid bounds and not obstacles
    return [pos for pos in neighbors if 0 <= pos[0] < grid.shape[0] and 0 <= pos[1] < grid.shape[1] and grid[tuple(pos)] == 0]

def reconstruct_path(node: Node) -> List[Tuple[int, int]]:
    # Reconstruct the path from end to start
    path = []
    current = node
    while current:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Reverse to get path from start to end

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

def visualize_path_text(grid_size: int, path: List[Tuple[int, int]]) -> str:
    # Create a text-based visualization of the path
    grid = [['.'] * grid_size for _ in range(grid_size)]
    for x, y in path:
        grid[x][y] = '*'
    grid[path[0][0]][path[0][1]] = 'S'  # Start
    grid[path[-1][0]][path[-1][1]] = 'E'  # End
    return '\n'.join(''.join(row) for row in grid)

def main():
    grid_size = 20
    grid = np.zeros((grid_size, grid_size))  # Create an empty grid
    
    start = np.array([4, 0])  # Starting position
    end = np.array([19, 19])  # Ending position
    
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

if __name__ == "__main__":
    main()
