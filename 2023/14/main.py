import fileinput
from copy import deepcopy


lines = [list(line.strip()) for line in fileinput.input()]

grid = deepcopy(lines)


def display(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            print(grid[i][j], end="")
        print()


def tilt_north(grid):
    grid = deepcopy(grid)
    for j in range(len(grid[0])):
        row_to_put = 0
        while row_to_put < len(grid) and grid[row_to_put][j] == "#":
            row_to_put += 1
        k = row_to_put
        while k < len(grid):
            if grid[k][j] == "#":
                row_to_put = k + 1
            elif grid[k][j] == "O":
                grid[k][j], grid[row_to_put][j] = grid[row_to_put][j], grid[k][j]
                row_to_put += 1
            k += 1
    return grid


def calculate_load(grid):
    s = 0
    for i in range(len(grid)):
        s += (len(grid) - i) * grid[i].count("O")
    return s


def rotate_grid_counterclockwise(grid):
    return [
        [grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]) - 1, -1, -1)
    ]


def rotate_grid_clockwise(grid):
    return [list(reversed(col)) for col in zip(*grid)]


# Tilt operations are not efficient because of rotations but I don't care


def tilt_west(grid):
    grid = rotate_grid_clockwise(grid)
    grid = tilt_north(grid)
    grid = rotate_grid_counterclockwise(grid)
    return grid


def tilt_south(grid):
    grid = rotate_grid_clockwise(grid)
    grid = rotate_grid_clockwise(grid)
    grid = tilt_north(grid)
    grid = rotate_grid_counterclockwise(grid)
    grid = rotate_grid_counterclockwise(grid)
    return grid


def tilt_east(grid):
    grid = rotate_grid_counterclockwise(grid)
    grid = tilt_north(grid)
    grid = rotate_grid_clockwise(grid)
    return grid


def tilt_4_ways(grid):
    grid = tilt_north(grid)
    grid = tilt_west(grid)
    grid = tilt_south(grid)
    grid = tilt_east(grid)
    return grid


def task1(grid):
    tilted_north = tilt_north(grid)
    return calculate_load(tilted_north)


def serialize(grid):
    return "".join(["".join(row) for row in grid])


def task2(grid):
    cycle_found = False
    iteration_to_load = {}
    serialized_to_iteration = {}
    iteration = 0
    serialized = None

    while not cycle_found:
        iteration += 1
        grid = tilt_4_ways(grid)
        load = calculate_load(grid)
        serialized = serialize(grid)

        if serialized not in serialized_to_iteration:
            serialized_to_iteration[serialized] = iteration
            iteration_to_load[iteration] = load
        else:
            cycle_found = True

    cycle_start = serialized_to_iteration[serialized]
    cycle_length = iteration - cycle_start
    offset = cycle_start + (1_000_000_000 - cycle_start) % cycle_length
    return iteration_to_load[offset]


print("Task 1:", task1(grid))
print("Task 2:", task2(grid))
