import fileinput
from copy import deepcopy
from itertools import groupby


lines = [line.strip() for line in fileinput.input()]

patterns = [
    [list(x) for x in group] for present, group in groupby(lines, key=bool) if present
]


def find_mirror_line_from_prepared_num_masks(nums, direction):
    candidates = []
    for i in range(len(nums) - 1):
        if nums[i] != nums[i + 1]:
            continue
        left, right = i, i + 1
        while 0 <= left and right < len(nums) and nums[left] == nums[right]:
            left -= 1
            right += 1
        left += 1
        right -= 1
        if left == 0 or right == len(nums) - 1:
            # only considering reflection when it reaches the end of pattern
            candidates.append((right - left + 1, direction, left, right, i))
    return candidates


def build_num_masks(pattern):
    height = len(pattern)
    width = len(pattern[0])
    nums = []
    for i in range(height):
        s = "".join([pattern[i][j] for j in range(width)])
        n = int(s.replace("#", "1").replace(".", "0"), 2)
        nums.append(n)
    return nums


def find_mirror_line_candidates(pattern):
    horizontal_nums = build_num_masks(pattern)
    # vertical masks are horizontal for transposed matrix
    vertical_nums = build_num_masks(list(zip(*pattern)))
    return find_mirror_line_from_prepared_num_masks(
        horizontal_nums, "h"
    ) + find_mirror_line_from_prepared_num_masks(vertical_nums, "v")


def task1(patterns):
    result = 0
    for i, pattern in enumerate(patterns, 1):
        # there is only 1 mirror line in the original pattern
        best = find_mirror_line_candidates(pattern)[0]
        width, typ, left, right, start = best
        if typ == "v":
            result += start + 1
        else:
            result += 100 * (start + 1)
    return result


def possible_smudge_coords(pattern):
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            if pattern[i][j] == "#":
                yield i, j


def task2(patterns):
    result = 0
    for pattern in patterns:
        # there is only 1 mirror line in the original pattern
        existing = find_mirror_line_candidates(pattern)[0]
        for i, j in possible_smudge_coords(pattern):
            # clearing smudge
            c = deepcopy(pattern)
            c[i][j] = "."
            new_candidates = [
                x for x in find_mirror_line_candidates(c) if x != existing
            ]
            if new_candidates:
                # cleared smudge might produce a few mirror lines,
                # we should pick one with the biggest reflection
                width, typ, left, right, start = max(new_candidates)
                if typ == "v":
                    result += start + 1
                else:
                    result += 100 * (start + 1)
                break
        else:
            assert False
    return result


print("Task 1:", task1(patterns))
print("Task 2:", task2(patterns))
