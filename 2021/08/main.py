import fileinput
from collections import Counter

notes = [
    (y[0].split(" "), y[1].split(" "))
    for y in [line.strip().split(" | ") for line in fileinput.input()]
]


def reverse_dict(d):
    return {v: k for k, v in d}


perfect_segment = {
    1: "CF",
    7: "ACF",
    4: "BCDF",
    2: "ACDEG",
    3: "ACDFG",
    5: "ABDFG",
    0: "ABCEFG",
    6: "ABDEFG",
    9: "ABCDFG",
    8: "ABCDEFG",
}


perfect_segment_to_number = {
    tuple(sorted(list(k))): v for v, k in perfect_segment.items()
}


perfect_mapping = reverse_dict(
    Counter(y for x in perfect_segment.values() for y in x).most_common()
)
perfect_mapping.pop(7)
perfect_mapping.pop(8)


def known_letters(known_mapping):
    return set(known_mapping.values())


def solve_note(inp, out):
    mapping = {}
    _1 = [x for x in inp if len(x) == 2][0]
    _4 = [x for x in inp if len(x) == 4][0]
    _7 = [x for x in inp if len(x) == 3][0]
    _8 = [x for x in inp if len(x) == 7][0]
    mapping["A"] = list(set(_7) - set(_1))[0]

    actual_mapping = reverse_dict(Counter(y for x in inp for y in x).most_common())
    for k in perfect_mapping.keys():
        mapping[perfect_mapping[k]] = actual_mapping[k]

    mapping["C"] = list(set(_1) - {mapping["F"]})[0]
    mapping["D"] = list(set(_4) - known_letters(mapping))[0]
    mapping["G"] = list(set(_8) - known_letters(mapping))[0]

    reverse_mapping = reverse_dict(mapping.items())
    number = 0
    for digit in out:
        key = tuple(sorted(list(reverse_mapping[x] for x in digit)))
        number = number * 10 + perfect_segment_to_number[key]
    return number


task1 = 0
task2 = 0
for note in notes:
    number = solve_note(*note)
    number_str = str(number)

    task1 += number_str.count("1")
    task1 += number_str.count("4")
    task1 += number_str.count("7")
    task1 += number_str.count("8")

    task2 += number


print(task1)
print(task2)
