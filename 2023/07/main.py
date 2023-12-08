import fileinput
from collections import Counter
from functools import cmp_to_key

lines = [line.strip() for line in fileinput.input("07/example1.txt")]
lines = [line.strip() for line in fileinput.input("07/input1.txt")]


def hand_strength(hand_cards, use_jokers):
    if use_jokers and hand_cards != "JJJJJ":
        jokers_count = hand_cards.count("J")
        most_common_card = Counter(hand_cards.replace("J", "")).most_common()[0][0]
        hand_cards = hand_cards.replace("J", most_common_card)
    mask = [count for (card, count) in Counter(hand_cards).most_common()]
    match mask:
        case [5]:
            return "7_five_of_a_kind"
        case [4, 1]:
            return "6_four_of_a_kind"
        case [3, 2]:
            return "5_full_house"
        case [3, 1, 1]:
            return "4_three_of_a_kind"
        case [2, 2, 1]:
            return "3_two_pairs"
        case [2, 1, 1, 1]:
            return "2_one_pair"
        case [1, 1, 1, 1, 1]:
            return "1_high_card"
        case _:
            print(mask)
            assert False


def card_strength(card):
    return "23456789TJQKA".index(card)


def card_strength_with_jokers(card):
    return "J23456789TQKA".index(card)


def parse(lines):
    return [(line.split()[0], int(line.split()[1])) for line in lines]


def task1(hands_and_bids, use_jokers=False):
    _card_strength = card_strength_with_jokers if use_jokers else card_strength

    def comparator(a, b):
        a_strength = hand_strength(a[0], use_jokers)
        b_strength = hand_strength(b[0], use_jokers)
        if a_strength < b_strength:
            return -1
        elif a_strength == b_strength:
            for c1, c2 in zip(map(_card_strength, a[0]), map(_card_strength, b[0])):
                if c1 < c2:
                    return -1
                elif c1 > c2:
                    return 1
        return 0

    hands_and_bids.sort(key=cmp_to_key(comparator))
    return sum([i * bid for i, (_, bid) in enumerate(hands_and_bids, 1)])


hands_and_bids = parse(lines)
print("Task 1:", task1(hands_and_bids, use_jokers=False))
print("Task 2:", task1(hands_and_bids, use_jokers=True))
