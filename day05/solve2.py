from functools import reduce

TRANSMAP = str.maketrans({'F': '0', 'B': '1', 'L': '0', 'R': '1'})


def main():
    input_ = load_input()
    print(part1(input_))
    print(part2(input_))


def load_input():
    with open('input.txt') as f:
        return [r.strip() for r in f.readlines()]


def part1(input_: list) -> int:
    return max(map(directions_to_id, input_))


def part2(input_: list) -> int:
    ticketed_ids = {directions_to_id(dir_) for dir_ in input_}
    return next(
        seat_id
        for seat_id in range(2**10)
        if seat_id not in ticketed_ids
        and seat_id + 1 in ticketed_ids
        and seat_id - 1 in ticketed_ids
    )


def directions_to_id(dirs: str) -> int:
    return int(dirs.translate(TRANSMAP), base=2)


if __name__ == '__main__':
    main()
