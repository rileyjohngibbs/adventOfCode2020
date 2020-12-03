from functools import reduce

TREE = '#'
OPEN = '.'


def main():
    input_ = load_input()
    print(part1(input_))
    print(part2(input_))


def load_input():
    with open('input.txt') as f:
        return [line.strip() for line in f.readlines()]


def part1(input_: list):
    return traverse(input_, 3, 1)


def part2(input_: list):
    return reduce(
        lambda x, y: x * traverse(input_, *y),
        [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)],
        1
    )


def traverse(input_: list, right: int, down: int) -> int:
    width = len(input_[0])
    tree_count = 0
    x, y = 0, 0
    while y < len(input_):
        if input_[y][x] == TREE:
            tree_count += 1
        x = (x + right) % width
        y += down
    return tree_count


if __name__ == '__main__':
    main()
