import fileinput
import operator
import typing as t
from functools import reduce

DEBUG = False


def _print(*args):
    if DEBUG:
        print(*args)


def parse_packet(bits_str):
    bits = "".join([bin(int(x, 16))[2:].zfill(4) for x in bits_str])

    def read_n_binary(index, n) -> t.Tuple[int, str, int]:
        return int(bits[index : index + n], 2), bits[index : index + n], index + n

    def read_packet(index) -> t.Tuple[dict, int]:
        version, _, index = read_n_binary(index, 3)
        type_id, _, index = read_n_binary(index, 3)
        _print(f"new packet: version: {version}, type_id: {type_id}")
        if type_id == 4:  # literal
            _print("parsing literal at", index)
            parts = ""
            while True:
                _, part, index = read_n_binary(index, 5)
                parts += part[1:]
                if part[0] == "0":
                    break
            value = int(parts, 2)
            _print("parsed value", value)
            return {
                "version": version,
                "type_id": type_id,
                "value": value,
            }, index
        else:
            _print("parsing operator at", index)
            length_type_id, _, index = read_n_binary(index, 1)
            _print("length_type_id:", length_type_id)

            if length_type_id == 0:
                total_length_in_bits, _, index = read_n_binary(index, 15)
                is_limit_reached = lambda i, _: i == total_length_in_bits  # noqa
            else:
                target_subpackets_count, _, index = read_n_binary(index, 11)
                is_limit_reached = lambda _, subpackets_count: subpackets_count == target_subpackets_count  # noqa

            subpackets = []
            start = index
            while not is_limit_reached(index - start, len(subpackets)):
                subpacket, index = read_packet(index)
                _print("parsed subpacket at", index, subpacket)
                subpackets.append(subpacket)

            return {
                "version": version,
                "type_id": type_id,
                "subpackets": subpackets,
            }, index

    return read_packet(0)[0]


def aggregated_version_number(packet):
    return packet["version"] + sum(map(aggregated_version_number, packet.get("subpackets", [])))


def evaluate(packet):
    match packet['type_id']:
        case 0:
            return sum(map(evaluate, packet['subpackets']))
        case 1:
            return reduce(operator.mul, map(evaluate, packet['subpackets']))
        case 2:
            return min(map(evaluate, packet['subpackets']))
        case 3:
            return max(map(evaluate, packet['subpackets']))
        case 4:
            return packet['value']
        case 5:
            first, second = list(map(evaluate, packet['subpackets']))
            return 1 if first > second else 0
        case 6:
            first, second = list(map(evaluate, packet['subpackets']))
            return 1 if first < second else 0
        case 7:
            first, second = list(map(evaluate, packet['subpackets']))
            return 1 if first == second else 0
        case _:
            raise Exception(f"Not implemented: {packet['type_id']}")


for line in fileinput.input():
    line = line.strip()
    packet = parse_packet(line)
    print(line)
    print("Task 1:", aggregated_version_number(packet))
    print("Task 2:", evaluate(packet))
