import fileinput
from itertools import groupby
import re
from collections import deque

lines = [line.strip() for line in fileinput.input()]


def to_int_list(s):
    return list(map(int, re.findall(r"\d+", s)))


def parse(lines):
    data = [list(x) for non_empty, x in groupby(lines, key=bool) if non_empty]
    seeds = to_int_list(data[0][0])
    conversions = []
    for d in data[1:]:
        name = d[0][:-1]
        rules = []
        for x in d[1:]:
            d_range_start, s_range_start, range_len = to_int_list(x)
            rules.append(
                {
                    "range_len": range_len,
                    "src_start": s_range_start,
                    "src_end": s_range_start + range_len,
                    "dst_start": d_range_start,
                }
            )
        conversions.append({"name": name, "rules": rules})
    return seeds, conversions


def task1_simple(seeds, conversions):
    result = 1e35
    for seed in seeds:
        next_value = seed
        for conversion in conversions:
            for rule in conversion["rules"]:
                if rule["src_start"] <= next_value < rule["src_end"]:
                    next_value = rule["dst_start"] + (next_value - rule["src_start"])
                    break
        result = min(result, next_value)
    return result


def solve(seed_ranges, conversions):
    def _solve(seed_range):
        result = float("inf")
        q = deque([[seed_range, 0]])
        while q:
            current_range, level = q.popleft()
            if level == len(conversions):
                result = min(result, current_range[0])
                continue
            current_start, current_end = current_range
            for rule in conversions[level]["rules"]:
                src_start = rule["src_start"]
                src_end = rule["src_end"]
                dst_start = rule["dst_start"]
                range_len = rule["range_len"]
                if current_end < src_start or src_end <= current_start:  # No overlap
                    continue
                elif src_start <= current_start <= current_end < src_end:
                    offset = current_start - src_start
                    q.append(
                        [
                            (
                                dst_start + offset,
                                dst_start + offset + current_end - current_start,
                            ),
                            level + 1,
                        ]
                    )
                    break
                elif current_start < src_start <= current_end < src_end:
                    offset = current_end - src_start
                    q.append([(dst_start, dst_start + offset), level + 1])
                    # the rest should be processed on a current level
                    q.append([(current_start, src_start - 1), level])
                    break
                elif src_start <= current_start < src_end <= current_end:
                    offset = current_start - src_start
                    q.append([(dst_start + offset, dst_start + range_len - 1), level + 1])
                    # the rest should be processed on a current level
                    q.append([(src_end, current_end), level])
                    break
                elif current_start < src_start <= src_end <= current_end:
                    q.append([(dst_start, dst_start + range_len), level + 1])
                    # the rest should be processed on a current level
                    q.append([(src_end, current_end), level])
                    q.append([(current_start, src_start), level])
                    break
            else:
                # didn't find any intersection so proceeding with current range 1 level deeper
                q.append([current_range, level + 1])
        return result

    return min(_solve(seed_range) for seed_range in seed_ranges)


def task1(seeds, conversions):
    seed_ranges = [(seed, seed + 1) for seed in seeds]
    return solve(seed_ranges, conversions)


def task2(seeds, conversions):
    seed_ranges = [(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)]
    return solve(seed_ranges, conversions)


seeds, conversions = parse(lines)

# print("Task 1 simple:", task1_simple(seeds, conversions))
print("Task 1:", task1(seeds, conversions))
print("Task 2:", task2(seeds, conversions))
