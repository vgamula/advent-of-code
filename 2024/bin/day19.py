import fileinput
from functools import cache

lines = [line.strip() for line in fileinput.input() if line.strip()]

patterns = set(lines[0].split(", "))
towels = lines[1:]


@cache
def check(towel):
    if not towel:
        return 1
    r = 0
    for pattern in patterns:
        if towel.startswith(pattern):
            r += check(towel[len(pattern) :])
    return r


def task1():
    r = 0
    for towel in towels:
        if check(towel):
            r += 1
    return r


def task2():
    r = 0
    for towel in towels:
        r += check(towel)
    return r


print("Task 1:", task1())
print("Task 2:", task2())
