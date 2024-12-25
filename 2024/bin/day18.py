import fileinput
import heapq
from collections import defaultdict

falling_bytes = [
    [int(x) for x in line.strip().split(",")]
    for line in fileinput.input()
    if line.strip()
]

n = 71
# n = 7

start = (0, 0)
end = (n - 1, n - 1)


def print_grid(grid):
    for i in range(n):
        for j in range(n):
            print(grid[(i, j)], end="")
        print()


def search(grid):
    visited = set()
    pq = [(0, start)]
    while pq:
        cost, (i, j) = heapq.heappop(pq)
        if (i, j) in visited:
            continue
        visited.add((i, j))
        if (i, j) == end:
            return cost
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and grid[(ni, nj)] != "#":
                heapq.heappush(pq, (cost + 1, (ni, nj)))
    return None


def task1(k):
    grid = defaultdict(lambda: ".")
    for j, i in falling_bytes[:k]:
        grid[(i, j)] = "#"
    return search(grid)


def task2():
    left = 0
    right = len(falling_bytes) - 1
    while left <= right:
        mid = (left + right) // 2
        if task1(mid) is not None:
            left = mid + 1
        else:
            right = mid - 1
    return falling_bytes[left - 1]


print("Task 1:", task1(1024))
print("Task 2:", ",".join(map(str, task2())))
