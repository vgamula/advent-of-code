import fileinput
import re
from functools import lru_cache

lines = [line.strip() for line in fileinput.input()]


def adjacent_coords(i, j):
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < len(lines) and 0 <= nj < len(lines[0]):
                yield ni, nj


@lru_cache
def numbers_in_row(i):
    return [
        (start := m.start(0), end := m.end(0), int(lines[i][start:end]))
        for m in re.finditer("\d+", lines[i])
    ]


def task1():
    processed = set()
    res = 0
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j].isdigit() or lines[i][j] == ".":
                continue
            for ni, nj in adjacent_coords(i, j):
                for start, end, num in numbers_in_row(ni):
                    if start <= nj < end and (ni, start, end) not in processed:
                        processed.add((ni, start, end))
                        res += num
    return res


def adjacent_gear_ratio(i, j) -> (int, int):
    processed = set()
    d = 1
    for ni, nj in adjacent_coords(i, j):
        for start, end, num in numbers_in_row(ni):
            if start <= nj < end and (ni, start, end) not in processed:
                processed.add((ni, start, end))
                d *= num
    return len(processed), d


def task2():
    res = 0
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j] == "*":
                n, s = adjacent_gear_ratio(i, j)
                if n == 2:
                    res += s
    return res


print("Task 1:", task1())
print("Task 2:", task2())
