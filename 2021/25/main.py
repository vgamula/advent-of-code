import fileinput
from collections import deque
from copy import deepcopy

state = [list(line.strip()) for line in fileinput.input()]
n = len(state)
m = len(state[0])


def step(state):
    new_state = deepcopy(state)
    q = deque()
    for i in range(n):
        for j in range(m):
            if new_state[i][j] == ">" and new_state[i][(j + 1) % m] == ".":
                q.append((i, j))
    while q:
        i, j = q.popleft()
        new_state[i][j] = "."
        new_state[i][(j + 1) % m] = ">"
    for i in range(n):
        for j in range(m):
            if new_state[i][j] == "v" and new_state[(i + 1) % n][j] == ".":
                q.append((i, j))
    while q:
        i, j = q.popleft()
        new_state[i][j] = "."
        new_state[(i + 1) % n][j] = "v"
    return new_state


def print_state(state):
    print("\n".join("".join(line) for line in state))


def solve(state):
    prev_state = state
    i = 0
    while True:
        i += 1
        new_state = step(prev_state)
        if new_state == prev_state:
            return i
        prev_state = new_state


print(solve(state))
