import fileinput
import re
from collections import defaultdict


lines = [line.strip() for line in fileinput.input()]
sequence = lines[0]
parts = sequence.split(",")


def hash(s):
    part_hash = 0
    for c in s:
        part_hash += ord(c)
        part_hash *= 17
        part_hash %= 256
    return part_hash


def search_or_none(regex, s, convert_fn):
    tmp = re.search(regex, s)
    if tmp:
        return convert_fn(tmp[0])
    return None


def task1(parts):
    return sum(hash(part) for part in parts)


def task2(parts):
    boxes = defaultdict(list)
    for i, part in enumerate(parts):
        label = search_or_none(r"\w+", part, str)
        operation = search_or_none(r"-|=", part, str)
        focal_length = search_or_none(r"\d+", part, int)
        target_box = hash(label)

        if operation == "=":
            for lense in boxes[target_box]:
                if lense[0] == label:
                    lense[1] = focal_length
                    break
            else:
                boxes[target_box].append([label, focal_length])
        elif operation == "-":
            boxes[target_box] = [
                lense for lense in boxes[target_box] if lense[0] != label
            ]

    focusing_power = 0
    for box_id, lenses in boxes.items():
        for i, (lense_label, focal_length) in enumerate(lenses, 1):
            focusing_power += (box_id + 1) * i * focal_length

    return focusing_power


print("Task 1:", task1(parts))
print("Task 2:", task2(parts))
