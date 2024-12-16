import os
import fileinput
from copy import deepcopy


DEBUG = bool(os.environ.get('DEBUG', 'False').lower() == 'true')


lines = [line.strip() for line in fileinput.input()]

grid = [list(l) for l in lines[:lines.index('')]]
commands = ''.join([l for l in lines[lines.index('')+1:]])
n = len(grid)
m = len(grid[0])



def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def grid_to_dict(grid):
    result = {}
    for i in range(n):
        for j in range(m):
            result[(i, j)] = grid[i][j]
    return result


def find_start_i_j(grid):
    for i in range(n):
        for j in range(m):
            if grid[i][j] == '@':
                return i, j
    assert False, 'Start not found'


def parse_direction(command):
    match command:
        case '<': return (0, -1)
        case '>': return (0, 1)
        case '^': return (-1, 0)
        case 'v': return (1, 0)
    assert False


def debug_grid(grid):
    for i in range(n):
        for j in range(m):
            debug(grid[i][j],end='')
        debug()


def within_bounds(point):
    i, j = point
    return 0 <= i < n and 0 <= j < m


def move(point, direction):
    return point[0] + direction[0], point[1] + direction[1]


def get_value(grid, point):
    i, j = point
    return grid[i][j]


def find_last_empty_position(grid, starting_point, direction):
    current_point = move(starting_point, direction)
    while True:
        if not within_bounds(current_point) or ((current_value := get_value(grid, current_point)) == '#'):
            return None
        elif current_value == '.':
            return current_point
        elif current_value == 'O':
            current_point = move(current_point, direction)
        else:
            assert False


def swap_values(grid, p1, p2):
    i1, j1 = p1
    i2, j2 = p2
    grid[i1][j1], grid[i2][j2] = grid[i2][j2], grid[i1][j1]


def calculate_gps_scores_sum(grid):
    result = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'O':
                result += 100 * i + j
    return result


def task1(grid, commands):
    grid = deepcopy(grid)
    position = find_start_i_j(grid)
    for command in commands:
        i, j = position
        direction = parse_direction(command)
        point_in_front = ci, cj = move(position, direction)
        cell_in_front = get_value(grid, point_in_front)
        debug(cell_in_front)
        if cell_in_front == '.':
            swap_values(grid, position, point_in_front)
            position = point_in_front
        elif cell_in_front == '#':
            pass
        elif cell_in_front == 'O':
            empty_position = find_last_empty_position(grid, point_in_front, direction)
            if empty_position:
                swap_values(grid, point_in_front, empty_position)
                swap_values(grid, position, point_in_front)
                position = point_in_front
        debug(f'Command: {command}')
        debug_grid(grid)

    return calculate_gps_scores_sum(grid)


print('Task 1:', task1(grid, commands))
