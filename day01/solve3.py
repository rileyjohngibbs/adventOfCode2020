from solve import load_input


def main():
    input_ = load_input()
    print(part1(input_))
    print(part2(input_))


def part1(input_: list):
    return next(
        x * y
        for x in input_
        for y in input_
        if x + y == 2020
    )


def part2(input_: list):
    return next(
        x * y * z
        for x in input_
        for y in input_
        for z in input_
        if x + y + z == 2020
    )


if __name__ == '__main__':
    main()
