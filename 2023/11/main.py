import fileinput
from itertools import combinations


lines = [line.strip() for line in fileinput.input()]


def extract_and_scale_galaxy_coords(lines, scaling_factor):
    N = len(lines)
    has_galaxy_in_column = [False] * N
    has_galaxy_in_row = [False] * N
    running_empty_columns = []
    running_empty_rows = []
    for i in range(len(lines)):
        has_galaxy_in_column[i] = sum([lines[k][i] == "#" for k in range(N)]) > 0
        has_galaxy_in_row[i] = sum([lines[i][k] == "#" for k in range(N)]) > 0
        if i == 0:
            running_empty_columns.append(int(not has_galaxy_in_column[0]))
            running_empty_rows = [int(not has_galaxy_in_row[0])]
        else:
            running_empty_columns.append(
                running_empty_columns[-1] + int(not has_galaxy_in_column[i])
            )
            running_empty_rows.append(
                running_empty_rows[-1] + int(not has_galaxy_in_row[i])
            )
    scaling_factor -= 1
    coords = []
    for i in range(N):
        for j in range(N):
            if lines[i][j] == "#":
                scaled_pos = (
                    i + running_empty_rows[i] * scaling_factor,
                    j + running_empty_columns[j] * scaling_factor,
                )
                coords.append(scaled_pos)
    return coords


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_sum_of_shortest_distances(coords):
    return sum(manhattan(p1, p2) for p1, p2 in combinations(coords, 2))


def solve(lines, scaling_factor):
    return find_sum_of_shortest_distances(
        extract_and_scale_galaxy_coords(lines, scaling_factor)
    )


print("Task 1 (with 2):", solve(lines, 2))
print("Task 2 (with 10):", solve(lines, 10))
print("Task 2 (with 100):", solve(lines, 100))
print("Task 2 (with 1,000,000):", solve(lines, 1_000_000))
