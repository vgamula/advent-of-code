import fileinput

depths = [int(line.strip()) for line in fileinput.input()]


def task1(depths):
    result = 0
    for a, b in zip(depths, depths[1:]):
        result += b > a
    return result


def task2(depths):
    return task1([sum(depths[i : i + 3]) for i in range(len(depths))])


print(f"Task 1: {task1(depths)}")
print(f"Task 2: {task2(depths)}")
