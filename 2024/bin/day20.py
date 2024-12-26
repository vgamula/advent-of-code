import fileinput
from collections import Counter, deque
from functools import cache

maze = [list(line.strip()) for line in fileinput.input() if line.strip()]

n = len(maze)
m = len(maze[0])


def find_point(p):
    for i in range(n):
        for j in range(m):
            if maze[i][j] == p:
                return i, j
    assert False


start = find_point("S")
end = find_point("E")


def search(start):
    visited = set()
    cost = 0
    q = deque([(cost, start, [start])])
    while q:
        cost, (i, j), path = q.popleft()
        if (i, j) in visited:
            continue
        visited.add((i, j))
        if (i, j) == end:
            return cost, path
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and maze[ni][nj] != "#":
                q.append((cost + 1, (ni, nj), path + [(ni, nj)]))
    assert False


max_cost, initial_path = search(start)


@cache
def search_fast(start):
    visited = set()
    q = deque([(0, start)])
    while q:
        cost, (i, j) = q.popleft()
        if (i, j) in visited:
            continue
        visited.add((i, j))
        if (i, j) == end:
            return cost
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and maze[ni][nj] != "#":
                q.append((cost + 1, (ni, nj)))
    assert False


def solve(max_cheating_power):
    cnt = Counter()
    for start_cost, point in enumerate(initial_path):
        for di in range(-max_cheating_power, max_cheating_power + 1):
            for dj in range(-max_cheating_power, max_cheating_power + 1):
                i, j = point[0] + di, point[1] + dj
                cheating_cost = abs(di) + abs(dj)
                if (
                    0 <= i < n
                    and 0 <= j < m
                    and cheating_cost <= max_cheating_power
                    and maze[i][j] != "#"
                ):
                    full_cost = start_cost + cheating_cost + search_fast((i, j))
                    if max_cost - full_cost >= 100:
                        cnt[max_cost - full_cost] += 1
    return sum(cnt.values())


def solve_faster(max_cheating_power):
    from itertools import combinations

    distance_to_end = {p: max_cost - i - 1 for i, p in enumerate(initial_path)}

    r = 0
    for p1, p2 in combinations(initial_path, 2):
        if p1 == p2:
            continue
        i1, j1 = p1
        i2, j2 = p2
        di = i2 - i1
        dj = j2 - j1
        cheating_cost = abs(di) + abs(dj)
        if cheating_cost <= max_cheating_power:
            path_cost = (
                max_cost - distance_to_end[p1] + cheating_cost + distance_to_end[p2]
            )
            if max_cost - path_cost >= 100:
                r += 1
    return r


# print("Task 1:", solve(2))
# print("Task 2:", solve(20))

print("Faster Task 1:", solve_faster(2))
print("Faster Task 2:", solve_faster(20))
