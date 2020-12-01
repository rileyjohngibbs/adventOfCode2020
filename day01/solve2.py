def main():
    input_ = load_input()
    print(part1(input_))
    print(part2(input_))


def load_input():
    with open('input.txt') as f:
        text = f.readlines()
    return [int(row.strip()) for row in text]


def product_of_summing_pair(nums: set, sum_: int):
    for first in nums:
        if first < sum_ and sum_ - first in nums:
            return first * (sum_ - first)


def part1(input_: list):
    input_set = set(input_)
    for first in input_set:
        if 2020 - first in input_set:
            return first * (2020 - first)


def part2(input_: list):
    input_set = set(input_)
    for first in input_set:
        sub_product = product_of_summing_pair(input_set, 2020 - first)
        if sub_product is not None:
            return first * sub_product


if __name__ == '__main__':
    main()
