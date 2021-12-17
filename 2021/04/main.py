import fileinput
from collections import defaultdict


def partition(items, n):
    result = []
    for i in range(0, len(items), n):
        result.append(items[i : i + n])
    return result


raw_input = [line.strip() for line in fileinput.input() if line.strip()]

numbers_to_guess = list(map(int, raw_input[0].split(",")))
boards = [
    [list(map(int, filter(lambda z: z, x.split(" ")))) for x in y]
    for y in partition(raw_input[1:], 5)
]
board_marked_as_won = defaultdict(lambda: False)
number_to_boards = defaultdict(set)
marked_positions = defaultdict(lambda: False)

solution = []


for i in range(len(boards)):
    for j in range(5):
        for k in range(5):
            number = boards[i][j][k]
            number_to_boards[number].add(i)

for guess in numbers_to_guess:
    for board_id in number_to_boards[guess]:
        for j in range(5):
            for k in range(5):
                if boards[board_id][j][k] == guess:
                    marked_positions[(board_id, j, k)] = True
                    if not board_marked_as_won[board_id] and (
                        all(marked_positions[(board_id, j, x)] for x in range(5))
                        or all(marked_positions[(board_id, x, k)] for x in range(5))
                    ):
                        board_marked_as_won[board_id] = True
                        unmarked = 0
                        for j in range(5):
                            for k in range(5):
                                if not marked_positions[(board_id, j, k)]:
                                    unmarked += boards[board_id][j][k]
                        solution.append(unmarked * guess)


print(f"Task 1: {solution[0]}")
print(f"Task 2: {solution[-1]}")
