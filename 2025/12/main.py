import re

with open("input.txt") as f:
    text = f.read().strip()

parts = text.split("\n\n")


def task1():
    result = 0
    for line in parts[-1].split("\n"):
        nums = [*map(int, re.findall(r"\d+", line))]
        presents_area = sum(x * 9 for x in nums[2:])
        region_area = nums[0] * nums[1]
        result += presents_area <= region_area

    return result


print(f"Task 1: {task1()}")
