from collections import defaultdict
import fileinput
from copy import deepcopy

lines = [line.strip() for line in fileinput.input()]

matrix = defaultdict(lambda: defaultdict(lambda: "."))
n = 0
m = 0

i = 0
while i < len(lines):
    if lines[i] == "":
        i += 1
        break
    x, y = list(map(int, lines[i].split(",")))
    n = max(n, y)
    m = max(m, x)
    matrix[y][x] = "#"
    i += 1

n += 1
m += 1

folds = []
while i < len(lines):
    axis, value = lines[i].replace("fold along ", "").split("=")
    folds.append((axis, int(value)))
    i += 1


def print_matrix(matrix, n, m):
    for i in range(n):
        tmp = ""
        for j in range(m):
            tmp += matrix[i][j]
        print(tmp)


def print_fold(matrix, n, m, fold):
    ftype, fv = fold
    for i in range(n):
        tmp = ""
        for j in range(m):
            if ftype == "x" and j == fv:
                tmp += "|"
            else:
                tmp += matrix[i][j]
        if ftype == "y" and i == fv:
            print("-" * m)
        else:
            print(tmp)


for line in lines:
    if line == "":
        continue


def do_fold_y(matrix, n, m, y):
    new_matrix = defaultdict(lambda: defaultdict(lambda: "."))
    i = y
    while y >= 0:
        for j in range(m):
            new_value = (
                "." if matrix[i - y - 1][j] == matrix[i + y + 1][j] == "." else "#"
            )
            new_matrix[i - y - 1][j] = new_value
        y -= 1

    return new_matrix, i, m


def do_fold_x(matrix, n, m, x):
    new_matrix = defaultdict(lambda: defaultdict(lambda: "."))
    j = x
    while x >= 0:
        for i in range(n):
            new_value = (
                "." if matrix[i][j - x - 1] == matrix[i][j + x + 1] == "." else "#"
            )
            new_matrix[i][j - x - 1] = new_value
        x -= 1

    return new_matrix, n, j


def fold_matrix(matrix, n, m, fold, with_print=False):
    if with_print:
        print("folding matrix:", fold)
        print_fold(matrix, n, m, fold)

    if fold[0] == "x":
        matrix, n, m = do_fold_x(matrix, n, m, fold[1])
    else:
        matrix, n, m = do_fold_y(matrix, n, m, fold[1])

    if with_print:
        print("result:")
        print_matrix(matrix, n, m)

    return matrix, n, m


def matrix_values(matrix):
    r = 0
    for subm in matrix.values():
        r += list(subm.values()).count("#")
    return r


def task1(matrix, folds):
    matrix = deepcopy(matrix)
    nn = n
    mm = m
    for fold in folds[:1]:
        matrix, nn, mm = fold_matrix(matrix, nn, mm, fold)

    return matrix_values(matrix)


def task2(matrix, folds):
    matrix = deepcopy(matrix)
    nn = n
    mm = m
    for fold in folds:
        matrix, nn, mm = fold_matrix(matrix, nn, mm, fold)

    print_matrix(matrix, nn, mm)


print(task1(matrix, folds))
task2(matrix, folds)
