import math
import sys
import time
from typing import List, Tuple

def main(*args):
    input_ = load_input('test' in args)
    start = time.time()
    print(part1(input_, 'test' in args))
    mid = time.time()
    print(f'Part 1 time: {mid - start}')
    print(part2(input_, 'test' in args))
    end = time.time()
    print(f'Part 2 time: {end - mid}')


def load_input(test: bool = False) -> Tuple[int, List[str]]:
    filename = f'{"test" * test}input.txt'
    with open(filename) as f:
        first, second = [r.strip() for r in f.readlines()]
    return int(first), second.split(',')


def part1(input_: Tuple[int, List[str]], test: bool = False):
    earliest_time = input_[0]
    bus_ids = [int(b) for b in input_[1] if b.isdigit()]
    wait, bus_id = min((b - (earliest_time % b), b) for b in bus_ids)
    return wait * bus_id


def part2(input_: Tuple[int, List[str]], test: bool = False):
    t = 0
    interval = 1
    bases = [(int(b), i) for i, b in enumerate(input_[1]) if b.isdigit()]
    for base, mod in bases:
        while (t + mod) % base:
            t += interval
        interval = lcm(base, interval)
    return t


def lcm(a: int, b: int) -> int:
    return a * b // math.gcd(a, b)


if __name__ == '__main__':
    main(*sys.argv)
