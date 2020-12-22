import re
import sys
import time
from typing import Iterable, List, Optional, Set, Tuple, Union


def main(*args):
    start = time.time()
    input_ = load_input('test' in args)
    print(part1(input_, 'test' in args))
    mid = time.time()
    input_ = load_input('test' in args)
    print(f'Part 1 time: {mid - start}')
    print(part2(input_, 'test' in args))
    end = time.time()
    print(f'Part 2 time: {end - mid}')


def load_input(test: bool = False) -> List[List[int]]:
    filename = f'{"test" * test}input.txt'
    with open(filename) as f:
        decks = [p.strip().split('\n')[1:] for p in f.read().split('\n\n')]
    return [[int(c) for c in deck] for deck in decks]


def part1(input_: List[List[int]], test: bool = False) -> int:
    player1, player2 = input_
    while player1 and player2:
        card1, card2 = player1.pop(0), player2.pop(0)
        if card1 > card2:
            player1.extend([card1, card2])
        else:
            player2.extend([card2, card1])
    winner = player1 or player2
    deck_size = len(winner)
    score = sum(
        card * (deck_size - index)
        for index, card in enumerate(winner)
    )
    return score


def part2(input_: List[List[int]], test: bool = False) -> int:
    player1, player2 = input_
    player1, player2 = play_game(player1[:], player2[:])
    winner = player1 or player2
    deck_size = len(winner)
    score = sum(
        card * (deck_size - index)
        for index, card in enumerate(winner)
    )
    return score


def play_game(
        player1: List[int],
        player2: List[int],
) -> Tuple[List[int], List[int]]:
    states: Set[Tuple[Tuple[int, ...]]] = set()
    while player1 and player2:
        state = (tuple(player1), tuple(player2))
        if state in states:
            return player1 + player2, []
        else:
            states.add(state)
        card1, card2 = player1.pop(0), player2.pop(0)
        if card1 > len(player1) or card2 > len(player2):
            if card1 > card2:
                player1.extend([card1, card2])
            else:
                player2.extend([card2, card1])
        else:
            sub1, sub2 = play_game(player1[:card1], player2[:card2])
            if sub1:
                player1.extend([card1, card2])
            else:
                player2.extend([card2, card1])
    return player1, player2


if __name__ == '__main__':
    main(*sys.argv)
