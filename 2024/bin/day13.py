import fileinput
import re

lines = [line.strip() for line in fileinput.input() if line.strip()]


def extract_x_y(s):
    return list(map(int, re.findall(r"(\d+)", s)))


machines = []
for ii in range(len(lines) // 3):
    i = ii * 3
    machines.append(
        {
            "Button1": extract_x_y(lines[i]),
            "Button2": extract_x_y(lines[i + 1]),
            "Prize": extract_x_y(lines[i + 2]),
        }
    )


def solve_using_sympy(not_more_than_100=True, delta=0):
    from sympy import symbols, Eq, solve

    result = 0
    for m in machines:
        a, b = symbols("a b", integer=True)
        eq1 = Eq(m["Button1"][0] * a + m["Button2"][0] * b, m["Prize"][0] + delta)
        eq2 = Eq(m["Button1"][1] * a + m["Button2"][1] * b, m["Prize"][1] + delta)
        solution = solve((eq1, eq2), (a, b))
        if solution and (not not_more_than_100 or (solution[a] <= 100 and solution[b] <= 100)):
            result += 3 * solution[a] + solution[b]
    return result


def solve_using_cramers_rule(not_more_than_100=True, delta=0):
    result = 0
    for m in machines:
        a1 = m["Button1"][0]
        b1 = m["Button2"][0]
        c1 = m["Prize"][0] + delta
        a2 = m["Button1"][1]
        b2 = m["Button2"][1]
        c2 = m["Prize"][1] + delta
        if a1 * b2 - b1 * a2 == 0:
            continue
        x = (c1 * b2 - b1 * c2) / (a1 * b2 - b1 * a2)
        y = (a1 * c2 - c1 * a2) / (a1 * b2 - b1 * a2)
        if x.is_integer() and y.is_integer() and (not not_more_than_100 or (x <= 100 and y <= 100)):
            result += 3 * int(x) + int(y)
    return result


print("Task 1:", solve_using_cramers_rule(not_more_than_100=True, delta=0))
print("Task 2:", solve_using_cramers_rule(not_more_than_100=False, delta=10000000000000))
