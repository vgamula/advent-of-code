import fileinput
import heapq
import itertools

maze = [list(line.strip()) for line in fileinput.input() if line.strip()]
n = len(maze)
m = len(maze[0])


def find_start_i_j():
    for i in range(n):
        for j in range(m):
            if maze[i][j] == "S":
                return i, j
    assert False


LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

possible_directions_from = {
    LEFT: [UP, DOWN, LEFT],
    RIGHT: [UP, DOWN, RIGHT],
    UP: [LEFT, RIGHT, UP],
    DOWN: [LEFT, RIGHT, DOWN],
}


def get_value(p):
    i, j = p
    return maze[i][j]


def within_bounds(point):
    i, j = point
    return 0 <= i < n and 0 <= j < m


def move(point, direction):
    return point[0] + direction[0], point[1] + direction[1]


def print_maze(visited_points):
    visited_points = set(visited_points)
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i, j) in visited_points:
                print("+", end="")
            else:
                print(maze[i][j], end="")
        print()


def task1():
    start = find_start_i_j()
    pq = [(0, start, RIGHT, [start])]
    min_distance_to = {start: 0}
    while pq:
        cost, p, direction, path = heapq.heappop(pq)
        min_distance_to[p] = cost
        if not within_bounds(p):
            continue
        if get_value(p) == "#":
            continue
        if get_value(p) == "E":
            return cost
        for next_direction in possible_directions_from[direction]:
            next_cost = cost + (1 if direction == next_direction else 1001)
            next_point = move(p, next_direction)
            if next_point not in min_distance_to or next_cost < min_distance_to[next_point]:
                heapq.heappush(pq, (next_cost, next_point, next_direction, path + [next_point]))
    assert False


print("Task 1:", best_cost := task1())


def task2(best_cost):
    possible_paths = []
    start = find_start_i_j()
    pq = [(0, start, RIGHT, [start])]
    min_distance_to = {start: {RIGHT: 0}}
    while pq:
        cost, p, direction, path = heapq.heappop(pq)
        if not within_bounds(p):
            continue
        if get_value(p) == "#":
            continue
        if cost > best_cost:
            continue
        if get_value(p) == "E":
            possible_paths.append(path[:])
            continue
        for next_direction in possible_directions_from[direction]:
            next_cost = cost + (1 if direction == next_direction else 1001)
            next_point = move(p, next_direction)
            if (
                next_point not in min_distance_to
                or next_direction not in min_distance_to[next_point]
                or next_cost <= min_distance_to[next_point][next_direction]
            ):
                if next_point not in min_distance_to:
                    min_distance_to[next_point] = {}
                min_distance_to[next_point][next_direction] = next_cost
                heapq.heappush(pq, (next_cost, next_point, next_direction, path + [next_point]))
    visited_points = set(itertools.chain(*possible_paths))
    return len(visited_points)


print("Task 2:", task2(best_cost))
