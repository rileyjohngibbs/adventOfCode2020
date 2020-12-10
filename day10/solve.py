from collections import Counter
from functools import reduce
from typing import Dict, List


def main():
    input_ = load_input()
    assert len(input_) == len(set(input_))
    print(part1(input_))
    print(part2(input_))


def load_input() -> List[int]:
    with open('input.txt') as f:
        return [int(r.strip()) for r in f.readlines()]


def part1(input_: List[int]) -> int:
    ord_ad = [0] + sorted(input_) + [max(input_) + 3]
    counter = Counter(b - a for a, b in zip(ord_ad[:-1], ord_ad[1:]))
    return counter[1] * counter[3]


def part2(input_: List[int]) -> int:
    ord_ad = [0] + sorted(input_) + [max(input_) + 3]
    cluster_length = 1
    cluster_counts = []
    for a, b in zip(ord_ad[:-1], ord_ad[1:]):
        if b - a == 3:
            if cluster_length > 1:
                count = spacer_counter(cluster_length)
                cluster_counts.append(count)
                cluster_length = 1
        else:
            cluster_length += 1
    return reduce(lambda a, b: a * b, cluster_counts)


def memoize(func):
    memo = {}
    def wrapper(n):
        if n in memo:
            value = memo[n]
        else:
            value = func(n)
            memo[n] = value
        return value
    return wrapper


@memoize
def spacer_counter(n: int) -> int:
    if n == 2:
        value = 1
    elif n == 3:
        value = 2
    elif n == 4:
        value = 4
    elif n == 5:
        value = 7
    else:
        value = (
            2 * spacer_counter(n-1)
            - spacer_counter(n-2)
            + 2**(n-5) + 1
        )
    return value


if __name__ == '__main__':
    main()
