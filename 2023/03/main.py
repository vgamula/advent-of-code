import fileinput
import re

lines = [line.strip() for line in fileinput.input()]


def adjacent_coords(i, j):
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == dj == 0:
                continue
            ni, nj = i + di, j + dj
            if 0 <= ni < len(lines) and 0 <= nj < len(lines[0]):
                yield ni, nj


def task1():
    processed = set()
    res = 0
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if lines[i][j].isdigit() or lines[i][j] == ".":
                continue
            for di, dj in adjacent_coords(i, j):
                # lots of duplicate work but I don't care
                for m in re.finditer("\d+", lines[di]):
                    start, end = m.start(0), m.end(0)
                    if start <= dj < end and (di, start, end) not in processed:
                        processed.add((di, start, end))
                        res += int(lines[di][start:end])
    return res


def adjacent_gear_ratio(i, j) -> (int, int):
    processed = set()
    d = 1
    for di, dj in adjacent_coords(i, j):
        for m in re.finditer("\d+", lines[di]):
            start, end = m.start(0), m.end(0)
            if start <= dj < end and (di, start, end) not in processed:
                processed.add((di, start, end))
                d *= int(lines[di][start:end])
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
