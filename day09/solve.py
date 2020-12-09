from typing import List, Tuple


def main():
    input_ = load_input()
    print(part1(input_))
    print(part2(input_))


class OrderedList(list):

    def __init__(self, *args, size=25, **kwargs):
        self.oldest = 0
        self.newest = -1
        self.size = size
        super().__init__(*args, **kwargs)

    def add(self, value: int):
        self.newest += 1
        self.oldest = max(0, self.newest - (self.size - 1))
        self.append((value, self.newest))
        self.sort(key=lambda ele: ele[0])
        self.trim_old_values()

    def trim_old_values(self):
        for index, (number, row) in enumerate(self):
            if row < self.oldest:
                self[index:index+1] = []
                break


def load_input() -> List[int]:
    with open('input.txt') as f:
        return [int(r.strip()) for r in f.readlines()]


def part1(input_: List[int]) -> int:
    return find_invalid_number(input_)


def part2(input_: List[int]) -> int:
    invalid_number = find_invalid_number(input_)
    sequence = find_sum_sequence(input_, invalid_number)
    return min(sequence) + max(sequence)


def find_invalid_number(input_: List[int]) -> int:
    ol = OrderedList()
    for number in input_:
        if len(ol) >= ol.size:
            try:
                i, j = find_sum_pair(ol, number)
            except ValueError:
                break
        ol.add(number)
    else:
        raise ValueError()
    return number


def find_sum_pair(
        numbers: OrderedList,
        target: int
) -> Tuple[int, int]:
    i, j = 0, -1
    while numbers[i][0] + numbers[j][0] != target or numbers[i][0] == numbers[j][0]:
        if numbers[i][0] + numbers[j][0] > target:
            j -= 1
        else:
            i += 1
        if i == len(numbers) + j:
            raise ValueError()
    return numbers[i], numbers[j]


def find_sum_sequence(numbers: List[int], target: int) -> List[int]:
    i, j = 0, 1
    total = numbers[i] + numbers[j]
    while total != target:
        if total > target:
            total -= numbers[i]
            i += 1
        elif total < target:
            j += 1
            total += numbers[j]
    sequence = numbers[i:j+1]
    return sequence


if __name__ == '__main__':
    main()
