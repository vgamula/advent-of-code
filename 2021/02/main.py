import fileinput

commands = []
for line in fileinput.input():
    command, value = line.strip().split(" ")
    commands.append((command, int(value)))


def task1(commands):
    horizontal = 0
    depth = 0
    for command, value in commands:
        if command == "forward":
            horizontal += value
        elif command == "down":
            depth += value
        elif command == "up":
            depth -= value
        else:
            assert False
    return horizontal * depth


def task2(commands):
    horizontal = 0
    depth = 0
    aim = 0
    for command, value in commands:
        if command == "forward":
            horizontal += value
            depth += aim * value
        elif command == "down":
            aim += value
        elif command == "up":
            aim -= value
        else:
            assert False
    return horizontal * depth


print(f"Task 1: {task1(commands)}")
print(f"Task 2: {task2(commands)}")
