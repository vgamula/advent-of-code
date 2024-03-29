from collections import defaultdict
import fileinput

lines = [line.strip() for line in fileinput.input()]


def parse_games(lines):
    games = []
    for line in lines:
        game_id = int(line[line.index(" ") : line.index(":")])
        subgames = []
        for subset in line[line.index(":") + 1 :].split(";"):
            for cubes in subset.split(","):
                num, color = cubes.strip().split(" ")
                subgames.append((int(num), color))
        games.append((game_id, subgames))
    return games


def task1(games):
    res = 0
    for game_id, subgames in games:
        stats = defaultdict(int)
        for num, color in subgames:
            stats[color] = max(stats[color], num)
        if stats["red"] <= 12 and stats["green"] <= 13 and stats["blue"] <= 14:
            res += game_id
    return res


def task2(games):
    res = 0
    for _, subgames in games:
        stats = defaultdict(int)
        for num, color in subgames:
            stats[color] = max(stats[color], num)
        res += stats["red"] * stats["green"] * stats["blue"]
    return res


games = parse_games(lines)
print("Task 1:", task1(games))
print("Task 2:", task2(games))
