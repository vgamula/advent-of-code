import fileinput
from collections import Counter

report = [line.strip() for line in fileinput.input()]


def task1(report):
    m = len(report[0])
    gamma = 0
    epsilon = 0
    for j in range(m):
        counter = Counter([x[j] for x in report])
        gamma = (gamma << 1) | int(counter.most_common(1)[0][0])
        epsilon = (epsilon << 1) | int(counter.most_common()[-1][0])
    print(gamma, epsilon)
    return gamma * epsilon


def find_value(considered_values: list, position: int, find_most_common: bool) -> int:
    bits = Counter([x[position] for x in considered_values])

    if find_most_common:
        bit_to_keep = bits.most_common()[0][0]
        if bits["0"] == bits["1"]:
            bit_to_keep = "1"
    else:
        bit_to_keep = bits.most_common()[-1][0]
        if bits["0"] == bits["1"]:
            bit_to_keep = "0"

    to_keep = [x for x in considered_values if x[position] == bit_to_keep]
    if len(to_keep) == 1:
        return to_keep[0]
    return find_value(to_keep, position + 1, find_most_common)


def task2(report):
    oxygen_rating = int(find_value(report, 0, find_most_common=True), 2)
    co2_rating = int(find_value(report, 0, find_most_common=False), 2)
    print(oxygen_rating, co2_rating)
    return oxygen_rating * co2_rating


print(f"Task 1: {task1(report)}")
print(f"Task 2: {task2(report)}")
