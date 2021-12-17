import fileinput
from collections import defaultdict

mx = 0
my = 0

segments = []

for line in fileinput.input():
    line = line.strip()
    c1, c2 = line.split(" -> ")

    c1 = tuple(map(int, c1.split(",")))
    c2 = tuple(map(int, c2.split(",")))

    segments.append((c1, c2))


grid1 = defaultdict(int)
grid2 = defaultdict(int)


def is_horizontal_or_vertical_line(c1, c2):
    x1, y1 = c1
    x2, y2 = c2
    return x1 == x2 or y1 == y2


def produce_points_between(c1, c2):
    x1, y1 = c1
    x2, y2 = c2
    if not (x1 == x2 or y1 == y1 or (x1 == y1 and x2 == y2) or (x1 == y2 and x2 == y1)):
        return

    if x1 == x2:
        dx = 0
    else:
        dx = 1 if x1 < x2 else -1

    if y1 == y2:
        dy = 0
    else:
        dy = 1 if y1 < y2 else -1

    while True:
        yield x1, y1
        x1 += dx
        y1 += dy

        if (x1, y1) == (x2, y2):
            yield x1, y1
            return


for c1, c2 in segments:
    for point in produce_points_between(c1, c2):
        if is_horizontal_or_vertical_line(c1, c2):
            grid1[point] += 1
        grid2[point] += 1

t1 = 0
t2 = 0


def count(grid):
    res = 0
    for v in grid.values():
        if v >= 2:
            res += 1
    return res


print(f"Task 1: {count(grid1)}")
print(f"Task 1: {count(grid2)}")
