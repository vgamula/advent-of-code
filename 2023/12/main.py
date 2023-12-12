import fileinput
import re
from functools import lru_cache
from itertools import starmap


lines = [line.strip() for line in fileinput.input()]


def parse(lines):
    result = []
    for line in lines:
        pattern, nums_str = line.split(" ")
        nums = [*map(int, re.findall(r"\d+", nums_str))]
        result.append((pattern, nums))
    return result


def solve_bruteforce(pattern, nums):
    def inner(i, s):
        if i == len(pattern):
            replaced = re.sub(r"\.+", "_", s).strip("_")
            if [len(x) for x in replaced.split("_")] == nums:
                return 1
            return 0
        if pattern[i] == "?":
            return inner(i + 1, s + ".") + inner(i + 1, s + "#")
        else:
            return inner(i + 1, s + pattern[i])

    return inner(0, "")


def solve_dp(pattern, nums):
    pattern = pattern + "."

    @lru_cache
    def inner(i, current_group_size, nums_idx):
        if i == len(pattern):
            return 1 if nums_idx == len(nums) else 0

        if (
            current_group_size > 0
            and nums_idx < len(nums)
            and current_group_size > nums[nums_idx]
        ):
            return 0

        ans = 0
        if pattern[i] == "#" or pattern[i] == "?":
            ans += inner(i + 1, current_group_size + 1, nums_idx)
        if pattern[i] == "." or pattern[i] == "?":
            if current_group_size == 0:
                ans += inner(i + 1, 0, nums_idx)
            elif nums_idx < len(nums) and current_group_size == nums[nums_idx]:
                ans += inner(i + 1, 0, nums_idx + 1)
        return ans

    return inner(0, 0, 0)


def task1(rows):
    return sum(starmap(solve_dp, rows))


def task2(rows):
    return sum(solve_dp("?".join([pattern] * 5), nums * 5) for pattern, nums in rows)


rows = parse(lines)
print("Task 1:", task1(rows))
print("Task 2:", task2(rows))
