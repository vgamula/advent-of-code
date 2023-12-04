import fileinput
import re
from collections import defaultdict


lines = [line.strip() for line in fileinput.input()]


def parse_cards(lines):
    cards = []
    for i, line in enumerate(lines, 1):
        nums = line[line.index(':') + 1:]
        winning_numbers, numbers_i_have = nums.split('|')
        cards.append({
            'id': i,
            'winning_numbers': [int(n) for n in re.findall(r'\d+', winning_numbers)],
            'numbers_i_have': [int(n) for n in re.findall(r'\d+', numbers_i_have)]
        })
    return cards


def task1(cards):
    s = 0
    for card in cards:
        if (c := len(set(card['winning_numbers']) & set(card['numbers_i_have']))) > 0:
            s += 2**(c - 1)
    return s


def task2(cards):
    cards_i_have = defaultdict(lambda: 1)
    for card in cards:
        winning_numbers_on_card = len(set(card['winning_numbers']) & set(card['numbers_i_have']))
        for i in range(card['id'], min(len(cards), card['id'] + winning_numbers_on_card)):
            cards_i_have[i + 1] += cards_i_have[card['id']]
    return sum(cards_i_have.values())


cards = parse_cards(lines)
print('Task 1:', task1(cards))
print('Task 2:', task2(cards))
