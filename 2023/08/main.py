import fileinput
import math
import re
from itertools import cycle


lines = [line.strip() for line in fileinput.input("08/input1.txt")]


def parse(lines):
    instructions = lines[0]
    transitions = {}
    for line in lines[2:]:
        node, left, right = [*re.findall(r"\w{3}", line)]
        transitions[node] = (left, right)
    return instructions, transitions


def steps_until_end(instructions, transitions, start, is_end_predicate):
    current = start
    n = 0
    for ins in cycle(instructions):
        if is_end_predicate(current):
            break
        n += 1
        current = transitions[current][ins == "R"]
    return n


def task1(instructions, transitions):
    return steps_until_end(
        instructions, transitions, start="AAA", is_end_predicate=lambda x: x == "ZZZ"
    )


def task2(instructions, transitions):
    steps = [
        steps_until_end(
            instructions,
            transitions,
            start=start,
            is_end_predicate=lambda x: x.endswith("Z"),
        )
        for start in transitions.keys()
        if start.endswith("A")
    ]
    return math.lcm(*steps)


instructions, transitions = parse(lines)
print("Task 1:", task1(instructions, transitions))
print("Task 2:", task2(instructions, transitions))
