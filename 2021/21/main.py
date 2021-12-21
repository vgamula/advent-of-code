import sys
from collections import Counter
from dataclasses import dataclass
from functools import cache

sys.setrecursionlimit(1000)

p1_position = int(input().split(" ")[-1])
p2_position = int(input().split(" ")[-1])


@dataclass(unsafe_hash=True)
class Player:
    score: int
    position: int

    def move_to(self, score_sum):
        position = self.position + score_sum
        position = (position % 10) + 10 * (position % 10 == 0)
        score = self.score + position
        return Player(score, position)


def task1(p1_position, p2_position):
    def dice():
        rolls = 0
        current_point = 0

        current_sum = 0
        while True:
            current_point += 1
            if current_point > 1000:
                current_point -= 1000
            current_sum += current_point
            rolls += 1

            if rolls % 3 == 0:
                yield current_sum, rolls
                current_sum = 0

    p1 = Player(0, p1_position)
    p2 = Player(0, p2_position)

    for i, (current_sum, rolls) in enumerate(dice()):
        if i % 2 == 0:
            p1 = p1.move_to(current_sum)
        else:
            p2 = p2.move_to(current_sum)

        if p1.score >= 1000:
            return p2.score * rolls
        elif p2.score >= 1000:
            return p1.score * rolls


print("Task 1:", task1(p1_position, p2_position))


combinations = []
for i in range(1, 4):
    for j in range(1, 4):
        for k in range(1, 4):
            combinations.append(i + j + k)


def task2(p1_position, p2_position):
    @cache
    def count_win_universes(p1, p2, player_to_play):
        wins = Counter()

        for rolls in combinations:
            p1_tmp = p1
            p2_tmp = p2
            if player_to_play == 1:
                p1_tmp = p1_tmp.move_to(rolls)
            else:
                p2_tmp = p2_tmp.move_to(rolls)

            if p1_tmp.score >= 21:
                wins[1] += 1
            elif p2_tmp.score >= 21:
                wins[2] += 1
            else:
                wins += count_win_universes(p1_tmp, p2_tmp, 3 - player_to_play)
        return wins

    return max(count_win_universes(Player(0, p1_position), Player(0, p2_position), 1).values())


print("Task 2:", task2(p1_position, p2_position))
