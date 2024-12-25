import fileinput
import re

lines = [line.strip() for line in fileinput.input() if line.strip()]


def extract_first_num(s):
    r = re.search(r"\d+", s)
    assert r is not None
    return int(r.group())


def extract_program_code(s) -> list[int]:
    return [int(x) for x in re.findall(r"\d+", s)]  # noqa


A = extract_first_num(lines[0])
B = extract_first_num(lines[1])
C = extract_first_num(lines[2])
program_code = extract_program_code(lines[3])


def task1(A, B, C, program_code):
    pc = 0
    output = []
    while pc + 1 < len(program_code):
        instruction = program_code[pc]
        combo_operand = program_code[pc + 1]

        literal_value = combo_operand
        if 0 <= combo_operand <= 3:
            combo_value = combo_operand
        elif combo_operand == 4:
            combo_value = A
        elif combo_operand == 5:
            combo_value = B
        elif combo_operand == 6:
            combo_value = C
        else:
            combo_value = 0

        if instruction == 0:  # adv
            A = A // (2**combo_value)
        elif instruction == 1:  # bxl
            B ^= literal_value
        elif instruction == 2:  # bst
            B = combo_value % 8
        elif instruction == 3 and A != 0:  # jnz
            pc = literal_value
            continue
        elif instruction == 4:  # bxc
            B ^= C
        elif instruction == 5:  # out
            output.append(combo_value % 8)
        elif instruction == 6:  # bdv
            B = A // (2**combo_value)
        elif instruction == 7:  # bsv
            C = A // (2**combo_value)
        pc += 2
    return output


print("Task 1:")
print(*task1(A, B, C, program_code), sep=",")


def task2(program_code):
    def find(i, a):
        result = task1(a, 0, 0, program_code)
        # print(i, a, result)
        if result == program_code:
            return a
        elif result == program_code[-i:] or i == 0:
            for n in range(8):
                tmp_res = find(i + 1, 8 * a + n)
                if tmp_res is not None:
                    return tmp_res
        return None

    return find(0, 0)


print("Task 2:", task2(program_code))
