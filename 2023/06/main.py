import re
import fileinput

lines = [line.strip() for line in fileinput.input()]


def task1(times, distances):
    d = 1
    for time, distance in zip(times, distances):
        s = 0
        for speed in range(1, time):
            if (time - speed) * speed > distance:
                s += 1
        d *= s
    return d


times = list(map(int, re.findall(r"\d+", lines[0])))
distances = list(map(int, re.findall(r"\d+", lines[1])))
print("Task 1:", task1(times, distances))


time = int("".join([c for c in lines[0] if c.isdigit()]))
distance = int("".join([c for c in lines[1] if c.isdigit()]))
print("Task 2:", task1([time], [distance]))
