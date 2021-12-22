import fileinput
from collections import defaultdict

lines = [line.strip() for line in fileinput.input()]


commands = []
for line in lines:
    command, *dimensions = line.replace("x=", "").replace(",y=", " ").replace(",z=", " ").replace("..", " ").split()
    commands.append((command, tuple(map(int, dimensions))))


def task1(commands):
    switched_on = set()
    for command, (x1, x2, y1, y2, z1, z2) in commands:
        for x in range(max(x1, -50), min(x2, 50) + 1):
            for y in range(max(y1, -50), min(y2, 50) + 1):
                for z in range(max(z1, -50), min(z2, 50) + 1):
                    coord = (x, y, z)
                    if command == "on":
                        switched_on.add(coord)
                    elif command == "off" and coord in switched_on:
                        switched_on.remove(coord)
    return len(switched_on)


print("Task 1:", task1(commands))


def find_intersection(cube1, cube2):
    ix1 = max(cube1[0], cube2[0])
    ix2 = min(cube1[1], cube2[1])
    iy1 = max(cube1[2], cube2[2])
    iy2 = min(cube1[3], cube2[3])
    iz1 = max(cube1[4], cube2[4])
    iz2 = min(cube1[5], cube2[5])
    if ix1 <= ix2 and iy1 <= iy2 and iz1 <= iz2:
        return ix1, ix2, iy1, iy2, iz1, iz2
    return None


def cube_size(cube):
    x1, x2, y1, y2, z1, z2 = cube
    return (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)


def task2(commands):
    cubes = defaultdict(int)

    for command, current_cube in commands:
        new_cubes = defaultdict(int)
        for existing_cube, count in cubes.items():
            intersection_cube = find_intersection(current_cube, existing_cube)
            if intersection_cube:
                new_cubes[intersection_cube] -= count

        if command == "on":
            new_cubes[current_cube] += 1

        for k, v in new_cubes.items():
            cubes[k] += v

    return sum(count * cube_size(cube) for cube, count in cubes.items())


print("Task 2:", task2(commands))
