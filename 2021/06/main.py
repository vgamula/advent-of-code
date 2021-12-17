from collections import Counter

lanternfish_ages = list(map(int, input().split(",")))

state = Counter(lanternfish_ages)


def step(state):
    new_state = Counter()
    for age, fish_count in state.items():
        if age == 0:
            new_state[8] += fish_count
            new_state[6] += fish_count
        else:
            new_state[age - 1] += fish_count
    return new_state


def simulate(state, days):
    for i in range(days):
        state = step(state)
    return state


def population(state):
    return sum(state.values())


print(f"18 days: {population(simulate(state, 18))}")
print(f"Task 1: {population(simulate(state, 80))}")
print(f"Task 2: {population(simulate(state, 256))}")
