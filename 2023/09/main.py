import fileinput

lines = [line.strip() for line in fileinput.input()]

sequences = [[*map(int, line.split())] for line in lines]


def solve(sequence):
    data = {0: sequence}
    rows_until_all_zeros = 0
    while not all([x == 0 for x in data[rows_until_all_zeros]]):
        rows_until_all_zeros += 1
        zipped = zip(
            data[rows_until_all_zeros - 1][:-1], data[rows_until_all_zeros - 1][1:]
        )
        data[rows_until_all_zeros] = [(b - a) for (a, b) in zipped]
    while rows_until_all_zeros > 0:
        rows_until_all_zeros -= 1
        data[rows_until_all_zeros].append(
            data[rows_until_all_zeros][-1] + data[rows_until_all_zeros + 1][-1]
        )
    return data[0][-1]


def task1(sequences):
    return sum(solve(sequence[:]) for sequence in sequences)


def task2(sequences):
    return sum(solve(sequence[::-1]) for sequence in sequences)


print("Task 1:", task1(sequences))
print("Task 2:", task2(sequences))