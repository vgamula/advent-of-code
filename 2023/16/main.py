import fileinput
from collections import deque
from itertools import starmap

A = [list(line.strip()) for line in fileinput.input("16/example1.txt")]
A = [list(line.strip()) for line in fileinput.input("16/input1.txt")]
height = len(A)
width = len(A[0])

LEFT = (0, -1)
UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)


def energized_tiles_count(start_position, direction):
    queue = deque([(start_position, direction)])
    energized = set()
    processed = set()

    # probably can be optimized using DP (?)
    while queue:
        action = queue.popleft()
        if action in processed:
            continue
        processed.add(action)

        pos, direction = action
        if not (0 <= pos[0] < height and 0 <= pos[1] < width):
            continue

        tile = A[pos[0]][pos[1]]
        energized.add(pos)
        next_directions = []

        if tile == ".":
            next_directions = [direction]
        elif tile == "-":
            if direction in [LEFT, RIGHT]:
                next_directions = [direction]
            elif direction in [UP, DOWN]:
                next_directions = [LEFT, RIGHT]
        elif tile == "|":
            if direction in [UP, DOWN]:
                next_directions = [direction]
            elif direction in [LEFT, RIGHT]:
                next_directions = [UP, DOWN]
        elif tile == "\\":
            next_direction = {
                UP: LEFT,
                DOWN: RIGHT,
                LEFT: UP,
                RIGHT: DOWN,
            }[direction]
            next_directions = [next_direction]
        elif tile == "/":
            next_direction = {
                UP: RIGHT,
                DOWN: LEFT,
                LEFT: DOWN,
                RIGHT: UP,
            }[direction]
            next_directions = [next_direction]
        else:
            assert False, action

        for next_direction in next_directions:
            next_pos = (pos[0] + next_direction[0], pos[1] + next_direction[1])
            queue.append((next_pos, next_direction))

    return len(energized)


def task1():
    return energized_tiles_count((0, 0), RIGHT)


def task2():
    to_check = []
    for i in range(height):
        to_check.append(((i, 0), RIGHT))
        to_check.append(((i, width - 1), LEFT))
    for j in range(width):
        to_check.append(((0, j), DOWN))
        to_check.append(((height - 1, j), UP))

    return max(starmap(energized_tiles_count, to_check))


print("Task 1:", task1())
print("Task 2:", task2())
