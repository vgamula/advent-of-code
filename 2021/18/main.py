import fileinput
import math
import typing as t
from dataclasses import dataclass

lines = [line.strip() for line in fileinput.input()]


@dataclass(init=False)
class SnailfishNumber:
    value: t.Union[int, None] = None
    left: t.Union[None, "SnailfishNumber"] = None
    right: t.Union[None, "SnailfishNumber"] = None
    parent: t.Union[None, "SnailfishNumber"] = None


def make_snailfish_number(raw_number, parent=None):
    num = SnailfishNumber()
    num.parent = parent
    if isinstance(raw_number, list):
        num.left = make_snailfish_number(raw_number[0], num)
        num.right = make_snailfish_number(raw_number[1], num)
    else:
        num.value = raw_number
    return num


def to_list(number: SnailfishNumber) -> t.Union[int, SnailfishNumber]:
    if number.value is not None:
        return number.value
    else:
        return [to_list(number.left), to_list(number.right)]


def find_nodes_to_explode(number: SnailfishNumber) -> t.List[SnailfishNumber]:
    depth_for_exlosion = 4
    nodes_to_explode = []

    def dfs(number, depth):
        if number is None or number.value is not None:
            return

        if depth < depth_for_exlosion:
            dfs(number.left, depth + 1)
            dfs(number.right, depth + 1)
        elif depth == depth_for_exlosion:
            nodes_to_explode.append(number)

    dfs(number, 0)

    def find_raw_nested_pair(number):
        while True:
            if number.left.value is not None and number.right.value is not None:
                break

            if number.left.value is None:
                number = number.left
            else:
                number = number.right
        return number

    return [find_raw_nested_pair(number) for number in nodes_to_explode]


def rightmost_number_literal(number):
    if number.value is not None:
        return number
    return rightmost_number_literal(number.right)


def leftmost_number_literal(number):
    if number.value is not None:
        return number
    return leftmost_number_literal(number.left)


def explode_snailfish_number(number_to_explode: SnailfishNumber) -> SnailfishNumber:
    # Left
    current_number = number_to_explode
    parent = number_to_explode.parent
    while parent and parent.left is current_number:
        current_number = parent
        parent = current_number.parent

    literal_for_left = rightmost_number_literal(parent.left) if parent else None
    if literal_for_left:
        literal_for_left.value += number_to_explode.left.value

    # Right
    current_number = number_to_explode
    parent = number_to_explode.parent
    while parent and parent.right is current_number:
        current_number = parent
        parent = current_number.parent

    literal_for_right = leftmost_number_literal(parent.right) if parent else None
    if literal_for_right:
        literal_for_right.value += number_to_explode.right.value

    # Parent
    new_num = make_snailfish_number(0, number_to_explode.parent)
    if number_to_explode is number_to_explode.parent.left:
        number_to_explode.parent.left = new_num
    else:
        number_to_explode.parent.right = new_num


def execute_split_snailfish_number(number: SnailfishNumber):
    splited_something = [False]

    def _split(number: SnailfishNumber):
        if splited_something[0]:  # circuit breaker
            return
        if number.value is None:
            _split(number.left)
            _split(number.right)
        elif number.value >= 10:
            number.left = make_snailfish_number(number.value // 2, number)
            number.right = make_snailfish_number(
                int(math.ceil(number.value / 2.0)), number
            )
            number.value = None
            splited_something[0] = True

    _split(number)
    return splited_something[0]


def execute_explode_snailfish_number(number: SnailfishNumber):
    exploded_something = False
    for to_explode in find_nodes_to_explode(number):
        explode_snailfish_number(to_explode)
        exploded_something = True

    return exploded_something


def reduce_snailfish_number(number):
    continue_reducing = True

    while continue_reducing:
        continue_reducing = False

        while execute_explode_snailfish_number(number):
            continue_reducing = True

        while execute_split_snailfish_number(number):
            continue_reducing = True
            break


def add(a: SnailfishNumber, b: SnailfishNumber) -> SnailfishNumber:
    num = SnailfishNumber()

    num.left = a
    a.parent = num

    num.right = b
    b.parent = num

    reduce_snailfish_number(num)

    return num


def snailfish_number_magnitude(number: SnailfishNumber) -> int:
    if number.value is not None:
        return number.value
    return 3 * snailfish_number_magnitude(number.left) + 2 * snailfish_number_magnitude(
        number.right
    )


total = None
for line in lines:
    py_numbers_list = eval(line)
    number = make_snailfish_number(py_numbers_list)
    reduce_snailfish_number(number)

    if total is None:
        total = number
    else:
        total = add(total, number)


print(to_list(total))
print("Task 1:", snailfish_number_magnitude(total))


max_magnitude = 0
for i in range(len(lines)):
    for j in range(i + 1, len(lines)):
        # a + b
        a = make_snailfish_number(eval(lines[i]))
        b = make_snailfish_number(eval(lines[j]))

        c = add(a, b)
        reduce_snailfish_number(c)
        max_magnitude = max(max_magnitude, snailfish_number_magnitude(c))

        # b + a
        a = make_snailfish_number(eval(lines[i]))
        b = make_snailfish_number(eval(lines[j]))

        c = add(b, a)
        max_magnitude = max(max_magnitude, snailfish_number_magnitude(c))


print("Task 2:", max_magnitude)


#
# =============TESTS=============
#


def test_explode():
    py_number_list = [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]]
    number = make_snailfish_number(py_number_list)
    for to_explode in find_nodes_to_explode(number):
        print("exploding:", to_explode)
        explode_snailfish_number(to_explode)
        print(to_list(number))


def test_add_and_reduce():
    a = make_snailfish_number([[[0, [4, 5]], [0, 0]], [[[4, 5], [2, 6]], [9, 5]]])
    b = make_snailfish_number([7, [[[3, 7], [4, 3]], [[6, 3], [8, 8]]]])
    c = add(a, b)
    print(to_list(a), "+", to_list(b), "=", to_list(c))
