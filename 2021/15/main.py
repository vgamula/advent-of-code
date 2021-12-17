import fileinput
import heapq
from collections import defaultdict

_grid = [list(map(int, line.strip())) for line in fileinput.input()]
n = len(_grid)
m = len(_grid[0])


def dijkstra(neighbors_fn, get_fn):
    q = [(0, (0, 0))]

    min_distance = defaultdict(lambda: 1e19)
    visited = set()

    while q:
        distance, position = heapq.heappop(q)
        min_distance[position] = min(min_distance[position], distance)
        visited.add(position)

        for neighbor in neighbors_fn(position):
            if neighbor not in visited:
                new_dist = min_distance[position] + get_fn(neighbor)
                if new_dist < min_distance[neighbor]:
                    min_distance[neighbor] = new_dist
                    heapq.heappush(q, (new_dist, neighbor))

    return min_distance


def neighbors(c):
    i, j = c
    for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        ii = i + di
        jj = j + dj
        if 0 <= ii < n and 0 <= jj < m:
            yield ii, jj


def get(coord):
    return _grid[coord[0]][coord[1]]


def neighbors_expanded(c):
    i, j = c
    for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        ii = i + di
        jj = j + dj
        if 0 <= ii < 5 * n and 0 <= jj < 5 * m:
            yield ii, jj


def get_expanded(c):
    i, j = c
    return (_grid[i % n][j % m] + i // n + j // m - 1) % 9 + 1


print(dijkstra(neighbors, get)[(n - 1, m - 1)])
print(dijkstra(neighbors_expanded, get_expanded)[(5 * n - 1, (5 * m - 1))])
