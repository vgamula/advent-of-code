import fileinput
from dataclasses import dataclass
from collections import deque

lines = [line.strip() for line in fileinput.input()]

scanners = []


DEBUG = False


def debug(*args):
    if DEBUG:
        print(*args)


@dataclass(unsafe_hash=True)
class Beacon:
    x: int
    y: int
    z: int

    def __sub__(self, other):
        return self.x - other.x, self.y - other.y, self.z - other.z

    def add_shift(self, shift):
        return Beacon(self.x + shift[0], self.y + shift[1], self.z + shift[2])


for line in lines:
    if line == "":
        continue
    elif line.startswith("---"):
        scanners.append([])
    else:
        scanners[-1].append(Beacon(*map(int, line.split(","))))


def all_rotations():
    yield lambda coord: Beacon(coord.x, coord.y, coord.z)
    yield lambda coord: Beacon(coord.x, -coord.z, coord.y)
    yield lambda coord: Beacon(coord.x, -coord.y, -coord.z)
    yield lambda coord: Beacon(coord.x, coord.z, -coord.y)

    yield lambda coord: Beacon(-coord.y, coord.x, coord.z)
    yield lambda coord: Beacon(coord.z, coord.x, coord.y)
    yield lambda coord: Beacon(coord.y, coord.x, -coord.z)
    yield lambda coord: Beacon(-coord.z, coord.x, -coord.y)

    yield lambda coord: Beacon(-coord.x, -coord.y, coord.z)
    yield lambda coord: Beacon(-coord.x, -coord.z, -coord.y)
    yield lambda coord: Beacon(-coord.x, coord.y, -coord.z)
    yield lambda coord: Beacon(-coord.x, coord.z, coord.y)

    yield lambda coord: Beacon(coord.y, -coord.x, coord.z)
    yield lambda coord: Beacon(coord.z, -coord.x, -coord.y)
    yield lambda coord: Beacon(-coord.y, -coord.x, -coord.z)
    yield lambda coord: Beacon(-coord.z, -coord.x, coord.y)

    yield lambda coord: Beacon(-coord.z, coord.y, coord.x)
    yield lambda coord: Beacon(coord.y, coord.z, coord.x)
    yield lambda coord: Beacon(coord.z, -coord.y, coord.x)
    yield lambda coord: Beacon(-coord.y, -coord.z, coord.x)

    yield lambda coord: Beacon(-coord.z, -coord.y, -coord.x)
    yield lambda coord: Beacon(-coord.y, coord.z, -coord.x)
    yield lambda coord: Beacon(coord.z, coord.y, -coord.x)
    yield lambda coord: Beacon(coord.y, -coord.z, -coord.x)


def get_distance(a: Beacon, b: Beacon) -> int:
    return (a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2


def beacons_distances(beacons):
    beacons = list(beacons)
    mapping = {}
    for i in range(len(beacons)):
        for j in range(i + 1, len(beacons)):
            if i == j:
                continue
            d = get_distance(beacons[i], beacons[j])
            mapping[d] = (beacons[i], beacons[j])
    return mapping


main_scanner_id = 0
main_scanner = set(scanners[main_scanner_id])
main_scanner_distances = beacons_distances(main_scanner)
queue = deque(range(1, len(scanners)))

scanner_positions = {0: (0, 0, 0)}


while queue:
    debug(queue)
    scanner_idx = queue.popleft()
    debug(f"Trying to match with scanner {scanner_idx}, queue-size: {len(queue)}")
    current_scanner_distances = beacons_distances(scanners[scanner_idx])
    intersection = set(main_scanner_distances.keys()) & set(current_scanner_distances.keys())

    if len(intersection) < 66:
        debug("Cannot match, moving to the end of queue", scanner_idx)
        queue.append(scanner_idx)
        continue

    for transformation in all_rotations():
        translated_points = list(map(transformation, scanners[scanner_idx]))
        found = False

        translated_distances = beacons_distances(translated_points)

        intersection = set(main_scanner_distances.keys()) & set(
            translated_distances.keys()
        )
        debug(len(intersection))

        # trying to align
        for distance in intersection:
            ma, mb = main_scanner_distances[distance]
            ta, tb = translated_distances[distance]

            # trying to match pairs of beacons with the same distance to each other
            if ma - ta == mb - tb:
                shift = ma - ta

                shifted_translated = set(map(lambda x: x.add_shift(shift), translated_points))
                common_beacons = set(main_scanner) & set(map(lambda x: x.add_shift(shift), translated_points))
                debug(f"Common beacons {len(common_beacons)}")

                if len(common_beacons) >= 12:
                    main_scanner = main_scanner.union(shifted_translated)
                    main_scanner_distances = beacons_distances(main_scanner)
                    found = True
                    scanner_positions[scanner_idx] = shift
                    debug(f"Matched {main_scanner_id} with {scanner_idx}")
                    break
        if found:
            break
    else:
        assert False


print('Task 1:', len(main_scanner))


def manhattan_distance(a, b):
    x1, y1, z1 = a
    x2, y2, z2 = b
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


max_dist = 0
for i in scanner_positions.keys():
    for j in scanner_positions.keys():
        max_dist = max(max_dist, manhattan_distance(scanner_positions[i], scanner_positions[j]))

print('Task 2:', max_dist)
