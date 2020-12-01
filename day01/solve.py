def main():
    input_ = load_input()
    print(part1(input_))
    print(part2(input_))


def load_input():
    with open('input.txt') as f:
        text = f.readlines()
    return [int(row.strip()) for row in text]


nums = load_input()

def part1(input_: list):
    nums = sorted(input_)
    i, j = 0, -1
    while nums[i] + nums[j] != 2020:
        if nums[i] + nums[j] > 2020:
            j -= 1
        else:
            i += 1
        if i == j:
            raise Exception()
    return nums[i] * nums[j]


def part2(input_: list):
    nums = sorted(input_)
    i, j, k = 0, 1, -1
    total = sum(nums[x] for x in (i, j, k))
    while total != 2020:
        if total > 2020:
            k -= 1
        else:
            j += 1
        if j == k:
            i += 1
            j, k = i + 1, -1
        total = sum(nums[x] for x in (i, j, k))
    return nums[i] * nums[j] * nums[k]


if __name__ == '__main__':
    main()
