import fileinput
import json
import math
from collections import deque


lines = [line.strip() for line in fileinput.input()]


A = [list(line) for line in lines]
N = -1, 0
S = 1, 0
W = 0, -1
E = 0, 1

possible_directions_from_pipe = {
    "|": {N, S},
    "-": {W, E},
    "L": {N, E},
    "J": {W, N},
    "7": {W, S},
    "F": {S, E},
    "S": {N, W, S, E},
}

possible_pipes_from_direction = {
    N: {*"|7FS"},
    S: {*"|LJS"},
    W: {*"-LFS"},
    E: {*"-J7S"},
}


def adjacent_pipes(position, A):
    i, j = position
    current_pipe = A[i][j]
    for direction in possible_directions_from_pipe[current_pipe]:
        di, dj = direction
        new_i, new_j = i + di, j + dj
        if 0 <= new_i < len(A) and 0 <= new_j < len(A[0]):
            new_pipe_type = A[i + di][j + dj]
            if new_pipe_type in possible_pipes_from_direction[direction]:
                yield i + di, j + dj


def find_longest_path():
    # a bit slow because we are going the same path from both directions
    possible_paths = []
    start = divmod("".join(lines).find("S"), len(A[0]))
    options = (start, {start}, [start], True)
    queue = deque([options])
    while queue:
        pos, visited, path, initial = queue.popleft()
        current_pipe = A[pos[0]][pos[1]]
        if current_pipe == "S" and not initial:
            possible_paths.append(path[:])
            continue
        for next_pos in adjacent_pipes(pos, A):
            if A[next_pos[0]][next_pos[1]] == "S" or next_pos not in visited:
                next_options = (
                    next_pos,
                    visited | {next_pos},
                    path + [next_pos],
                    False,
                )
                queue.append(next_options)
    longest_path = max(possible_paths, key=len)
    return longest_path


longest_path = find_longest_path()


print("Task 1:", len(longest_path) // 2)


def shoelace(points):
    # calculating polygon area using shoelace formula
    n = len(points)
    sum1 = 0
    sum2 = 0

    for i in range(0, n - 1):
        sum1 = sum1 + points[i][0] * points[i + 1][1]
        sum2 = sum2 + points[i][1] * points[i + 1][0]

    sum1 = sum1 + points[n - 1][0] * points[0][1]
    sum2 = sum2 + points[0][0] * points[n - 1][1]
    area = abs(sum1 - sum2) / 2
    return area


def task2(path):
    # Pick's theorem
    return math.ceil(shoelace(path) - len(path) / 2 + 1)


print("Task 2:", task2(longest_path))
