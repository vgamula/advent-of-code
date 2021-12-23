import heapq
from collections import defaultdict, Counter

DEBUG = True
DEBUG = False


def playable_character(state):
    for i, col in enumerate(state):
        for c in col:
            if c.isalpha():
                yield i, c
            break


perfect_column_for_character = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}

character_cost = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}


def debug(*args):
    if DEBUG:
        print(*args)


def validate_next_state(next_state, home_size):
    c = Counter()
    for col in next_state:
        for fish in col:
            c[fish] += 1
    assert c["A"] == c["B"] == c["C"] == c["D"] == home_size, next_state


def next_states(current_state, pc, home_size):
    playable_character_idx, character = pc

    # go left
    i = playable_character_idx - 1
    if playable_character_idx % 2 == 1 or playable_character_idx == len(current_state) - 1:
        cost = 1
    else:
        cost = 2 + home_size - len(current_state[playable_character_idx])
    i = playable_character_idx - 1

    started_at_home = playable_character_idx % 2 == 0 and 2 <= playable_character_idx <= 8

    while i >= 0:
        over_home_column = i % 2 == 0 and i != 0
        over_stop_column = i % 2 == 1 or i == 0

        if over_home_column and i != perfect_column_for_character[character]:
            pass
        elif over_home_column and i == perfect_column_for_character[character]:
            if current_state[i] == "":
                next_state = list(current_state)
                next_state[playable_character_idx] = next_state[playable_character_idx][1:]
                next_state[i] = character + next_state[i]
                next_cost = cost + home_size
                yield tuple(next_state), next_cost * character_cost[character]
            elif set(list(current_state[i])) == {character}:
                next_state = list(current_state)
                next_state[playable_character_idx] = next_state[playable_character_idx][1:]
                next_state[i] = character + next_state[i]
                next_cost = cost + home_size - len(list(current_state[i]))
                yield tuple(next_state), next_cost * character_cost[character]
        elif over_stop_column:
            if current_state[i] != "":
                break
            if started_at_home:
                next_state = list(current_state)
                next_state[playable_character_idx] = next_state[playable_character_idx][1:]
                next_state[i] = character + next_state[i]
                next_cost = cost
                yield tuple(next_state), next_cost * character_cost[character]
        else:
            assert False
        i -= 1
        cost += 1

    # go right
    i = playable_character_idx + 1
    if playable_character_idx % 2 == 1 or playable_character_idx == 0:
        cost = 1
    else:
        cost = 2 + home_size - len(current_state[playable_character_idx])
    i = playable_character_idx + 1

    while i < len(current_state):
        over_home_column = i % 2 == 0 and i != len(current_state) - 1
        over_stop_column = i % 2 == 1 or i == len(current_state) - 1

        if over_home_column and i != perfect_column_for_character[character]:
            pass
        elif i == perfect_column_for_character[character]:
            if current_state[i] == "":
                next_state = list(current_state)
                next_state[playable_character_idx] = next_state[playable_character_idx][1:]
                next_state[i] = character + next_state[i]
                next_cost = cost + home_size
                yield tuple(next_state), next_cost * character_cost[character]
            elif set(current_state[i]) == {character}:
                next_state = list(current_state)
                next_state[playable_character_idx] = next_state[playable_character_idx][1:]
                next_state[i] = character + next_state[i]
                next_cost = cost + home_size - len(list(current_state[i]))
                yield tuple(next_state), next_cost * character_cost[character]
        elif over_stop_column:
            if current_state[i] != "":
                break
            if started_at_home:
                next_state = list(current_state)
                next_state[playable_character_idx] = next_state[playable_character_idx][1:]
                next_state[i] = character + next_state[i]
                next_cost = cost
                yield tuple(next_state), next_cost * character_cost[character]
        else:
            assert False
        i += 1
        cost += 1


def dijkstra(state, home_size):
    min_cost = defaultdict(lambda: 1e18)
    pq = [(0, state)]
    heapq.heapify(pq)
    visited = set()

    while pq:
        current_cost, current_state = heapq.heappop(pq)

        if current_cost >= min_cost[current_state]:
            continue

        min_cost[current_state] = min(min_cost[current_state], current_cost)
        visited.add(current_state)

        if current_state == target_state:
            continue

        for pc in playable_character(current_state):
            for next_state, cost_to_next_state in next_states(current_state, pc, home_size):
                if next_state in visited:
                    continue
                validate_next_state(next_state, home_size)
                next_cost = min_cost[current_state] + cost_to_next_state
                if next_cost < min_cost[next_state]:
                    heapq.heappush(pq, (next_cost, next_state))

    return min_cost


def solve(initial_state, target_state):
    home_size = max(map(len, target_state))
    return dijkstra(initial_state, home_size)[target_state]


initial_state = ("", "", "BD", "", "BA", "", "CA", "", "DC", "", "")
target_state = ("", "", "AA", "", "BB", "", "CC", "", "DD", "", "")
print("Task 1:", solve(initial_state, target_state))

initial_state = ("", "", "BDDD", "", "BCBA", "", "CBAA", "", "DACC", "", "")
target_state = ("", "", "AAAA", "", "BBBB", "", "CCCC", "", "DDDD", "", "")
print("Task 2:", solve(initial_state, target_state))
