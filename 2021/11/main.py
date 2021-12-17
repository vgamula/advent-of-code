import fileinput
from copy import deepcopy
from collections import deque

energies = [list(map(int, list(line.strip()))) for line in fileinput.input()]
energies2 = deepcopy(energies)
n = len(energies)
m = len(energies[0])


def is_valid(ni, nj):
    return 0 <= ni < n and 0 <= nj < m


def adjacent_coords(i, j):
    for di in range(-1, 2):
        for dj in range(-1, 2):
            ni = i + di
            nj = j + dj
            if di == dj == 0:
                continue
            if is_valid(ni, nj):
                yield ni, nj


def step(state):
    new_state = deepcopy(state)
    flashed = set()
    future_flashes = deque()
    for i in range(n):
        for j in range(m):
            new_state[i][j] += 1
            if new_state[i][j] > 9:
                future_flashes.append((i, j))

    flashes_per_step = 0

    while future_flashes:
        for _ in range(len(future_flashes)):
            coord = future_flashes.popleft()
            i, j = coord

            if coord in flashed:
                continue

            flashed.add((i, j))
            new_state[i][j] = 0
            flashes_per_step += 1

            for ni, nj in adjacent_coords(i, j):
                c = (ni, nj)
                if c not in flashed:
                    new_state[ni][nj] += 1

        for i in range(n):
            for j in range(m):
                if new_state[i][j] > 9:
                    future_flashes.append((i, j))

    return new_state, flashes_per_step


def simulate(n, state):
    # print(0)
    # print("\n".join("".join(str(x)) for x in state))
    res = 0
    for i in range(n):
        # print(i + 1)
        state, flushes_per_round = step(state)
        res += flushes_per_round
        # print("flushes_per_round: ", i + 1, flushes_per_round)
        # print("\n".join("".join(str(x)) for x in state))
    print(res)


simulate(100, energies)


state = energies2
i = 0
while True:
    i += 1
    state, flushes_per_round = step(state)
    if flushes_per_round == n * m:
        print(i)
        break
