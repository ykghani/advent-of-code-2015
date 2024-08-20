'''
Advent of Code 2015 Day 18 - Like a GIF for your Yard
'''
from copy import deepcopy

file_path = 'd18_input.txt'
grid = []

# test_grid = ['.#.#.#',
#              '...##.',
#              '#....#',
#              '..#...',
#              '#.#..#',
#              '####..']

with open(file_path, 'r') as file: 
    for line in file: 
        line = line.strip()
        grid.append(list(line))

# for line in test_grid: 
#     grid.append(list(line))
        
def get_neighbors(grid, x, y):
    neighbors = []
    rows = len(grid)
    cols = len(grid[0])

    # Possible offsets for the eight neighbors
    offsets = [(-1, -1), (-1, 0), (-1, 1),
               (0, -1),         (0, 1),
               (1, -1), (1, 0), (1, 1)]

    for dx, dy in offsets:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols:  # Check if neighbor is within bounds
            neighbors.append(grid[nx][ny])

    return neighbors

STEPS = 100

part_two = True
if part_two: 
    grid[0][0] = '#'
    grid[0][len(grid) - 1] = '#'
    grid[len(grid) - 1][0] = '#'
    grid[len(grid) - 1][len(grid) - 1] = '#' 
    corners = [(0, 0), (0, len(grid[0]) - 1), (len(grid) - 1, 0), (len(grid) -1 , len(grid[0]) - 1)]

update_matrix = deepcopy(grid)
for _ in range(STEPS):
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            neighbors = get_neighbors(grid, i, j)
            if part_two: 
                if (i, j) in corners: 
                    continue
                else: 
                    if grid[i][j] == "#":
                        if neighbors.count('#') == 2 or neighbors.count('#') == 3: 
                            update_matrix[i][j] = '#'
                        else:
                            update_matrix[i][j] = '.'
                    else:
                        if neighbors.count('#') == 3:
                            update_matrix[i][j] = '#'
                        else:
                            update_matrix[i][j] = '.' 
                
    
    # grid = update_matrix.copy()
    grid = deepcopy(update_matrix)

lit_count = sum(row.count('#') for row in grid)
if part_two: 
    print(f"Part 2 answer: {lit_count}")
else: 
    print(f"Part 1 answer: {lit_count}")

        
        