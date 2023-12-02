from collections import defaultdict
import fileinput

lines = [line.strip() for line in fileinput.input()]


def parse_games(lines):
    games = []
    for line in lines:
        game_id = int(line[line.index(" ") : line.index(":")])
        sbs = []
        for subset in line[line.index(":") + 1 :].split(";"):
            sb = []
            for cubes in subset.split(","):
                num, color = cubes.strip().split(" ")
                sb.append((int(num), color))
            sbs.append(sb)
        games.append((game_id, sbs))
    return games


def task1(games):
    res = 0
    for game_id, subgames in games:
        stats = defaultdict(int)
        for subgame in subgames:
            for num, color in subgame:
                stats[color] = max(stats[color], num)
        if stats["red"] <= 12 and stats["green"] <= 13 and stats["blue"] <= 14:
            res += game_id
    return res


def task2(games):
    res = 0
    for _, subgames in games:
        stats = defaultdict(int)
        for subgame in subgames:
            for num, color in subgame:
                stats[color] = max(stats[color], num)
        res += stats["red"] * stats["green"] * stats["blue"]
    return res


games = parse_games(lines)
print("Task 1:", task1(games))
print("Task 2:", task2(games))
