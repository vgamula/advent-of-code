import fileinput

lines = [[*map(int,list(line.strip()))] for line in fileinput.input() if line.strip()]
data = lines[0]

assert len(data) % 2 == 1

def calculate_checksum(memory):
    checksum = 0
    for i in range(len(memory)):
        checksum += memory[i] * i
    return checksum


def task1(data):
    data = data.copy()
    idx = 0
    file_idx = len(data) - 1
    memory = []

    while idx <= file_idx:
        if idx % 2 == 0:
            file_id = idx // 2
            for _ in range(data[idx]):
                memory.append(file_id)
            idx += 1
        elif idx % 2 == 1 and data[idx] == 0:
            idx += 1
        elif idx % 2 == 1 and data[file_idx] == 0:
            file_idx -= 2
        elif idx % 2 == 1 and data[idx] > 0:
            file_id = file_idx // 2
            movable_count = min(data[idx], data[file_idx])
            for _ in range(movable_count):
                memory.append(file_id)
            data[idx] -= movable_count
            data[file_idx] -= movable_count
    return calculate_checksum(memory)

print('Task 1:', task1(data))


def task2(data):
    data = data.copy()
    detailed_memory = []
    for i in range(len(data)):
        file_id = i // 2
        # (free_space: int , blocks [(file_id, len)])
        if i % 2 == 0:
            detailed_memory.append((0, [(file_id, data[i])]))
        else:
            detailed_memory.append((data[i], []))

    movable_file_idx = len(data) - 1
    while movable_file_idx > 1:
        if data[movable_file_idx] > 0:
            file_to_move = detailed_memory[movable_file_idx][1][-1]
            potential_free_space_idx = 1
            # find block block with enough free space
            while potential_free_space_idx < movable_file_idx:
                if detailed_memory[potential_free_space_idx][0] >= data[movable_file_idx]:
                    break
                potential_free_space_idx += 2

            # if found - move file there
            if potential_free_space_idx < movable_file_idx:
                detailed_memory[potential_free_space_idx] = (
                    detailed_memory[potential_free_space_idx][0] - file_to_move[1],
                    detailed_memory[potential_free_space_idx][1] + [file_to_move]
                )
                detailed_memory[movable_file_idx] = (
                    detailed_memory[movable_file_idx][0] + file_to_move[1],
                    detailed_memory[movable_file_idx][1][:-1],
                )
                pass
        movable_file_idx -= 2

    # restore memory from detailed memory layour
    memory = []
    for (free_space), blocks in detailed_memory:
        for (file_id, size) in blocks:
            memory.extend([file_id] * size)
        if free_space:
            memory.extend([0] * free_space)

    return calculate_checksum(memory)

print('Task 2:', task2(data))
