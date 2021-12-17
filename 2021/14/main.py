import fileinput
from collections import Counter
from functools import lru_cache

lines = [line.strip() for line in fileinput.input()]

template = lines[0]
replacements = {}
for line in lines[2:]:
    f, t = line.split(" -> ")
    replacements[f] = t


@lru_cache(maxsize=None)
def count(pair, steps_left) -> Counter:
    if steps_left == 0 or pair not in replacements:
        return Counter()
    r = replacements[pair]
    return (
        Counter(r)
        + count(pair[0] + r, steps_left - 1)
        + count(r + pair[1], steps_left - 1)
    )


def solve(template, steps):
    answer_counter = sum(
        (count(template[i : i + 2], steps) for i in range(len(template) - 1)),
        start=Counter(template),
    )

    most = answer_counter.most_common()[0][1]
    least = answer_counter.most_common()[-1][1]

    return most - least


print(solve(template, 10))
print(solve(template, 40))
