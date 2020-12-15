import math
import sys
import time
from typing import Dict, List, Tuple

def main(*args):
    input_ = load_input('test' in args)
    start = time.time()
    print(part1(input_, 'test' in args))
    mid = time.time()
    print(f'Part 1 time: {mid - start}')
    print(part2(input_, 'test' in args))
    end = time.time()
    print(f'Part 2 time: {end - mid}')


def load_input(test: bool = False) -> List[int]:
    filename = f'{"test" * test}input.txt'
    with open(filename) as f:
        return [int(i) for i in f.read().strip().split(',')]


def part1(input_: List[int], test: bool = False) -> int:
    memory = {num: i + 1 for i, num in enumerate(input_[:-1])}
    current = input_[-1]
    for turn in range(len(input_), 2020):
        old, current = current, turn - memory.get(current, turn)
        memory[old] = turn
    return current


def part2(input_: List[int], test: bool = False) -> int:
    memory = {num: i + 1 for i, num in enumerate(input_[:-1])}
    current = input_[-1]
    for turn in range(len(input_), 30_000_000):
        old, current = current, turn - memory.get(current, turn)
        memory[old] = turn
    return current


if __name__ == '__main__':
    main(*sys.argv)
