import os
import fileinput
from copy import deepcopy


DEBUG = bool(os.environ.get("DEBUG", "False").lower() == "true")


lines = [line.strip() for line in fileinput.input()]


def build_extended_grid(lines):
    grid = []
    for line in lines:
        tmp = []
        for c in line:
            if c == "#":
                tmp.extend("#")
                tmp.extend("#")
            elif c == "O":
                tmp.append("[")
                tmp.append("]")
            elif c == ".":
                tmp.append(".")
                tmp.append(".")
            elif c == "@":
                tmp.append("@")
                tmp.append(".")
            else:
                assert False
        grid.append(tmp)
    return grid


grid = [list(l) for l in lines[: lines.index("")]]
grid_extended = build_extended_grid(lines[: lines.index("")])
commands = "".join([l for l in lines[lines.index("") + 1 :]])


def debug(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)


def find_start_i_j(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "@":
                return i, j
    assert False, "Start not found"


LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

command_to_direction = {
    "<": LEFT,
    ">": RIGHT,
    "^": UP,
    "v": DOWN,
}


def debug_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            debug(grid[i][j], end="")
        debug()


def within_bounds(grid, point):
    i, j = point
    return 0 <= i < len(grid) and 0 <= j < len(grid[0])


def move(point, direction):
    return point[0] + direction[0], point[1] + direction[1]


def get_value(grid, point):
    i, j = point
    return grid[i][j]


def swap_values(grid, p1, p2):
    i1, j1 = p1
    i2, j2 = p2
    grid[i1][j1], grid[i2][j2] = grid[i2][j2], grid[i1][j1]


def calculate_gps_scores_sum(grid):
    result = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] in "O[":
                result += 100 * i + j
    return result


def find_empty_position_horizontally(grid, starting_point, direction):
    current_point = move(starting_point, direction)
    while True:
        if not within_bounds(grid, current_point) or ((current_value := get_value(grid, current_point)) == "#"):
            return None
        elif current_value == ".":
            return current_point
        elif current_value in "[]O":
            current_point = move(current_point, direction)
        else:
            assert False


def task1(grid, commands):
    grid = deepcopy(grid)
    position = find_start_i_j(grid)
    for command in commands:
        i, j = position
        direction = command_to_direction[command]
        point_in_front = ci, cj = move(position, direction)
        cell_in_front = get_value(grid, point_in_front)
        debug(cell_in_front)
        if cell_in_front == ".":
            swap_values(grid, position, point_in_front)
            position = point_in_front
        elif cell_in_front == "#":
            pass
        elif cell_in_front == "O":
            empty_position = find_empty_position_horizontally(grid, point_in_front, direction)
            if empty_position:
                swap_values(grid, point_in_front, empty_position)
                swap_values(grid, position, point_in_front)
                position = point_in_front
        debug(f"Command: {command}")
        debug_grid(grid)

    return calculate_gps_scores_sum(grid)


print("Task 1:", task1(grid, commands))


def can_move_vertically(grid, position, direction, leftmost_positions):
    value = get_value(grid, position)
    if value == ".":
        return True
    if value == "#":
        return False
    if value == "]":
        leftmost_positions.add(move(position, LEFT))
        return can_move_vertically(grid, move(position, LEFT), direction, leftmost_positions) and (
            can_move_vertically(grid, move(move(position, direction), RIGHT), direction, leftmost_positions)
            if get_value(grid, move(position, direction)) == "["
            else can_move_vertically(grid, move(position, direction), direction, leftmost_positions)
        )
    if value == "[":
        leftmost_positions.add(position)
        return can_move_vertically(grid, move(position, direction), direction, leftmost_positions)
    assert False


def task2(grid, commands):  # noqa
    grid = deepcopy(grid)
    position = find_start_i_j(grid)
    for command in commands:
        i, j = position
        direction = command_to_direction[command]
        point_in_front = move(position, direction)
        cell_in_front = get_value(grid, point_in_front)
        if cell_in_front == ".":
            swap_values(grid, position, point_in_front)
            position = point_in_front
        elif cell_in_front == "#":
            pass
        elif cell_in_front in "[]":
            if direction == LEFT or direction == RIGHT:
                empty_position = find_empty_position_horizontally(grid, point_in_front, direction)
                if empty_position:
                    while empty_position != point_in_front:
                        next_position = move(empty_position, RIGHT if direction == LEFT else LEFT)
                        grid[empty_position[0]][empty_position[1]] = grid[next_position[0]][next_position[1]]
                        empty_position = next_position
                    grid[point_in_front[0]][point_in_front[1]] = "@"
                    grid[position[0]][position[1]] = "."
                    position = point_in_front
            elif direction == UP or direction == DOWN:
                leftmost_positions = set()
                can_move = (
                    can_move_vertically(grid, move(point_in_front, RIGHT), direction, leftmost_positions)
                    if cell_in_front == "["
                    else can_move_vertically(grid, point_in_front, direction, leftmost_positions)
                )
                if can_move:
                    leftmost_positions = sorted(leftmost_positions, reverse=direction == DOWN)
                    for l in leftmost_positions:
                        r = move(l, RIGHT)
                        swap_values(grid, l, move(l, direction))
                        swap_values(grid, r, move(r, direction))
                    swap_values(grid, position, point_in_front)
                    position = point_in_front
        debug(f"Command: {command}")
        debug_grid(grid)

    return calculate_gps_scores_sum(grid)


print("Task 2:", task2(grid_extended, commands))
