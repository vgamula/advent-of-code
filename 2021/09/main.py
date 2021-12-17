import collections
import fileinput
import operator
from functools import reduce

lines = [line.strip() for line in fileinput.input()]

n = len(lines)
m = len(lines[0])


def get(c):
    return int(lines[c[0]][c[1]])


def is_valid(p):
    return 0 <= p[0] < n and 0 <= p[1] < m


def adjacent_points(c):
    for dx, dy in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        x = c[0] + dx
        y = c[1] + dy
        p = (x, y)
        if is_valid(p):
            yield p


def adjacent_values_to_coord(c):
    for p in adjacent_points(c):
        yield get(p)


t1 = 0
for i in range(n):
    for j in range(m):
        p = i, j
        v = get(p)
        if all(v < x for x in adjacent_values_to_coord(p)):
            t1 += v + 1


basin_area = collections.defaultdict(int)
visited = set()


def traverse(p, start, visited):
    if p in visited or get(p) == 9:
        return
    visited.add(p)
    basin_area[start] += 1
    for np in adjacent_points(p):
        if np in visited or get(np) == 9:
            continue
        traverse(np, start, visited)


for i in range(n):
    for j in range(m):
        p = i, j
        if p in visited or get(p) == 9:
            continue
        else:
            traverse(p, p, visited)

t2 = reduce(operator.mul, sorted(list(basin_area.values()))[-3:])


print(t1)
print(t2)
