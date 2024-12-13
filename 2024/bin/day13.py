import fileinput
import re
from sympy import symbols, Eq, solve


lines = [line.strip() for line in fileinput.input() if line.strip()]

machines = []
for ii in range(len(lines) // 3):
    i = ii * 3
    machines.append(
        {
            "Button1": list(map(int, re.findall(r"X\+(\d+), Y\+(\d+)", lines[i])[0])),
            "Button2": list(map(int, re.findall(r"X\+(\d+), Y\+(\d+)", lines[i + 1])[0])),
            "Prize": list(map(int, re.findall(r"X=(\d+), Y=(\d+)", lines[i + 2])[0])),
        }
    )


def task1(not_more_than_100=True, delta=0):
    result = 0
    for machine in machines:
        a, b = symbols("a b", integer=True)
        eq1 = Eq(machine["Button1"][0] * a + machine["Button2"][0] * b, machine["Prize"][0] + delta)
        eq2 = Eq(machine["Button1"][1] * a + machine["Button2"][1] * b, machine["Prize"][1] + delta)
        solution = solve((eq1, eq2), (a, b))
        if solution and (not not_more_than_100 or (not_more_than_100 and solution[a] <= 100 and solution[b] <= 100)):
            result += 3 * solution[a] + solution[b]
    return result


print("Task 1:", task1(not_more_than_100=True, delta=0))
print("Task 2:", task1(not_more_than_100=False, delta=10000000000000))
