import fileinput
from functools import reduce

import z3

lines = [line.strip().split(" ") for line in fileinput.input()]


def translate(lines):
    print("w = 0")
    print("x = 0")
    print("y = 0")
    print("z = 0")

    def print_line(i, *args):
        print(f"{i + 1}:", *args)

    for i, line in enumerate(lines):
        if line[0] == "inp":
            print()
            print_line(i, f"{line[1]} = input()")
        elif line[0] == "add":
            print_line(i, f"{line[1]} += {line[2]}")
        elif line[0] == "mul":
            print_line(i, f"{line[1]} *= {line[2]}")
        elif line[0] == "div":
            print_line(i, f"{line[1]} //= {line[2]}")
        elif line[0] == "mod":
            print_line(i, f"{line[1]} %= {line[2]}")
        elif line[0] == "eql":
            print_line(i, f"{line[1]} = 1 if {line[1]} == {line[2]} else 0")


def is_num(x):
    try:
        int(x)
        return True
    except Exception:
        return False


# Learned z3 tricks on Reddit


def solve(lines, optimizer_fn):
    solver = z3.Optimize()
    zero = z3.BitVecVal(0, 64)
    one = z3.BitVecVal(1, 64)

    inputs = []
    for i in range(14):
        tmp = z3.BitVec(f"input_{i}", 64)
        solver.add(tmp >= 1)
        solver.add(tmp <= 9)
        inputs.append(tmp)
    inputs_iter = iter(inputs)

    state = {
        "w": zero,
        "x": zero,
        "y": zero,
        "z": zero,
    }

    for i, line in enumerate(lines):
        if line[0] == "inp":
            state[line[1]] = next(inputs_iter)
            continue

        tmp = z3.BitVec(f"tmp_{i}", 64)
        a1 = state[line[1]]
        if is_num(line[2]):
            a2 = int(line[2])
        else:
            a2 = state[line[2]]

        if line[0] == "add":
            solver.add(tmp == a1 + a2)
        elif line[0] == "mul":
            solver.add(tmp == a1 * a2)
        elif line[0] == "div":
            solver.add(a2 != 0)
            solver.add(tmp == a1 / a2)
        elif line[0] == "mod":
            solver.add(tmp == a1 % a2)
        elif line[0] == "eql":
            solver.add(tmp == z3.If(a1 == a2, one, zero))
        state[line[1]] = tmp

    solver.add(state["z"] == 0)

    tmp = reduce(lambda acc, x: acc * 10 + x, inputs)

    optimizer_fn(solver, tmp)

    assert solver.check() == z3.sat

    m = solver.model()
    return m.eval(tmp)


print("Task 1:", solve(lines, z3.Optimize.maximize))
print("Task 2:", solve(lines, z3.Optimize.minimize))
