import fileinput
from collections import defaultdict


data = [list(line.strip()) for line in fileinput.input() if line.strip()]
n = len(data)
m = len(data[0])


def get(point, safe=False):
    i, j = point
    if 0 <= i < n and 0 <= j < m:
        return data[i][j]
    elif not safe:
        raise IndexError(f'Get at wrong index i={i}, j={j}')
    return None


def neighbors(point):
    for di, dj in [
        (-1, 0),
        (0, -1),
        (1, 0),
        (0, 1),
    ]:
        ni, nj = point[0] + di, point[1] + dj
        if 0 <= ni < n and 0 <= nj < m:
            yield (ni, nj)


def build_garden():
    garden = defaultdict(set)
    plant_id = 0
    visited = set()
    def prepare_garden(plant_id, plant_type, point):
        if point in visited or get(point) != plant_type:
            return
        visited.add(point)
        garden[(plant_id, plant_type)].add(point)
        for neighbor in neighbors(point):
            prepare_garden(plant_id, plant_type, neighbor)
    for i in range(n):
        for j in range(m):
            point = i, j
            if point not in visited:
                plant_id += 1
                prepare_garden(plant_id, get(point), point)
    return garden


garden = build_garden()


def task1():
    def segment_perimeter(plant_type, plants):
        perimeter = 0
        for plant in plants:
            single_plant_perimeter = 4
            for neighbor in neighbors(plant):
                if neighbor in plants:
                    single_plant_perimeter -= 1
            perimeter += single_plant_perimeter
        return perimeter

    result = 0
    for ((_, plant_type), plants) in garden.items():
        result += segment_perimeter(plant_type, plants) * len(plants)
    return result


print('Task 1:', task1())


def task2():
    def sides_count(current, plant_group):
        # Number of sides = number of corners
        corners = 0
        for plant in plant_group:
            i, j = plant
            left = get((i, j - 1), safe=True)
            right = get((i, j + 1), safe=True)
            top = get((i - 1, j), safe=True)
            bottom = get((i + 1, j), safe=True)
            top_left = get((i - 1, j - 1), safe=True)
            top_right = get((i - 1, j + 1), safe=True)
            bottom_left = get((i + 1, j - 1), safe=True)
            bottom_right = get((i + 1, j + 1), safe=True)

            # acute
            if current != top and current != left:
                corners += 1
            if current != top and current != right:
                corners += 1
            if current != bottom and current != left:
                corners += 1
            if current != bottom and current != right:
                corners += 1

            # obtuse
            if current == top and current == left and current != top_left:
                corners += 1
            if current == top and current == right and current != top_right:
                corners += 1
            if current == bottom and current == left and current != bottom_left:
                corners += 1
            if current == bottom and current == right and current != bottom_right:
                corners += 1
        return corners

    result = 0
    for ((_, plant_type), plants) in garden.items():
        result += sides_count(plant_type, plants) * len(plants)
    return result


print('Task 2:', task2())
