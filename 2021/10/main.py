import fileinput

lines = [line.strip() for line in fileinput.input()]

open_brackets = {*"([{<"}

opposite_bracket = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}

bracket_cost = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def find_incomplete_character(line):
    stack = []
    for c in line:
        if c in open_brackets:
            stack.append(c)
        elif stack and stack[-1] == opposite_bracket[c]:
            stack.pop()
        else:
            return c
    return None


def task1(lines):
    cost = 0
    for line in lines:
        cost += bracket_cost.get(find_incomplete_character(line), 0)
    return cost


autocomplete_bracket_cost = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


def calculate_complete_score(line):
    stack = []
    for c in line:
        if c in open_brackets:
            stack.append(c)
        elif stack and stack[-1] == opposite_bracket[c]:
            stack.pop()
        else:
            return 0
    tmp = 0
    while stack and (c := stack.pop()):
        tmp = (5 * tmp) + autocomplete_bracket_cost[c]
    return tmp


def task2(lines):
    scores = []
    for line in lines:
        score = calculate_complete_score(line)
        if score:
            scores.append(score)
    return sorted(scores)[len(scores) // 2]


print(task1(lines))
print(task2(lines))
