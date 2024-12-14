import fileinput
import re
from copy import deepcopy
from collections import defaultdict

lines = [line.strip() for line in fileinput.input() if line.strip()]

width, height = 11, 7
width, height = 101, 103


def parse_robots(lines):
    robots = []
    for line in lines:
        x, y, velocity_x, velocity_y = list(map(int, re.findall(r'-?\d+', line)))
        robots.append({
            'x': x,
            'y': y,
            'velocity_x': velocity_x,
            'velocity_y': velocity_y,
        })
    return robots


robots = parse_robots(lines)


def calculate_safety_factor(state):
    quadrants = {
        'top_left': 0,
        'top_right': 0,
        'bottom_left': 0,
        'bottom_right': 0
    }
    mid_x = width // 2
    mid_y = height // 2
    for (y, x), count in state.items():
        if x == mid_x or y == mid_y:
            continue
        if x < mid_x and y < mid_y:
            quadrants['top_left'] += count
        elif x > mid_x and y < mid_y:
            quadrants['top_right'] += count
        elif x < mid_x and y > mid_y:
            quadrants['bottom_left'] += count
        elif x > mid_x and y > mid_y:
            quadrants['bottom_right'] += count
    safety_factor = 1
    for count in quadrants.values():
        safety_factor *= count
    return safety_factor


def print_state(state):
    for i in range(height):
        for j in range(width):
            if state[(i, j)] > 0:
                print('█', end='')
            else:
                print(' ', end='')
        print()


def task1(robots):
    robots = deepcopy(robots)
    iterations = 100
    state = defaultdict(int)
    for robot in robots:
        robot['x'] = (robot['x'] + (robot['velocity_x'] * iterations)) % width
        robot['y'] = (robot['y'] + (robot['velocity_y'] * iterations)) % height
        state[(robot['y'], robot['x'])] += 1
    return calculate_safety_factor(state)


def task2(robots):
    robots = deepcopy(robots)
    iterations = 10000
    state = defaultdict(int)
    for i in range(1, iterations + 1):
        for robot in robots:
            if i > 1:
                state[(robot['y'], robot['x'])] -= 1
            robot['x'] = (robot['x'] + robot['velocity_x']) % width
            robot['y'] = (robot['y'] + robot['velocity_y']) % height
            state[(robot['y'], robot['x'])] += 1
        print(f'----{i}----')
        print_state(state)


print('Task 1:', task1(robots))

# task2(robots)
