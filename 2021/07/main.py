positions = list(map(int, input().split(",")))


def task1(positions):
    positions = sorted(positions)

    return min(
        sum(abs(x - positions[len(positions) // 2]) for x in positions),
        sum(abs(x - positions[len(positions) // 2 + 1]) for x in positions),
    )


def arithm_progression_sum(a, b):
    x = abs(a - b)
    return (1 + x) * x // 2


def task2(positions):
    result = 1e18

    for i in range(max(positions) + 1):
        tmp = 0
        for j in range(len(positions)):
            tmp += arithm_progression_sum(i, positions[j])
        result = min(result, tmp)
    return result


print(task1(positions))
print(task2(positions))
