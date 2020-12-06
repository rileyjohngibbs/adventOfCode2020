from functools import reduce


def main():
    input_ = load_input()
    print(part1(input_))
    print(part2(input_))


def load_input():
    with open('input.txt') as f:
        return [g.split() for g in f.read().split('\n\n')]


def part1(input_: list):
    return sum(
        len(reduce(lambda a, b: a | set(b), group, set()))
        for group in input_
    )


def part2(input_: list):
    return sum(
        len(reduce(lambda a, b: a & set(b), group, set(group[0])))
        for group in input_
    )


if __name__ == '__main__':
    main()
