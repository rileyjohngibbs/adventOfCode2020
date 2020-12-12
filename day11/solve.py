import time
from typing import List, Optional

FLOOR = '.'
OCCUPIED = '#'
EMPTY = 'L'


def main():
    input_ = load_input()
    start = time.time()
    print(part1(input_))
    mid = time.time()
    print(f'Part 1 time: {mid - start}')
    print(part2(input_))
    end = time.time()
    print(f'Part 2 time: {end - mid}')


def load_input() -> List[int]:
    with open('input.txt') as f:
        return [r.strip() for r in f.readlines()]


def part1(input_: List[str]) -> int:
    new_grid = Grid([[c for c in row] for row in input_])
    grid = Grid([])
    while new_grid != grid:
        grid, new_grid = new_grid, new_grid.move_people()
    return grid.occupied


def part2(input_: List[str]) -> int:
    new_grid = Grid([[c for c in row] for row in input_])
    grid = Grid([])
    while new_grid != grid:
        grid, new_grid = new_grid, new_grid.move_people(visible=True)
    return grid.occupied


class Grid:

    def __init__(self, seats: List[List[str]], occupied: int = None):
        self.seats = seats
        if occupied is None:
            occupied = self.count_occupied()
        self.occupied = occupied

    def __eq__(self, other) -> bool:
        return self.occupied == other.occupied and self.seats == other.seats

    def __str__(self) -> str:
        return '\n'.join(''.join(r) for r in self.seats)

    def count_occupied(self) -> int:
        return len([s for r in self.seats for s in r if s == OCCUPIED])

    def move_people(self, visible: bool = False) -> List[List[str]]:
        if visible:
            metric = self.find_occupied_visible
        else:
            metric = self.find_occupied_adjacent
        occupied_count = 0
        new_seats = []
        for j, row in enumerate(self.seats):
            new_row = []
            new_seats.append(new_row)
            for i, seat in enumerate(row):
                occupied = metric(i, j)
                if seat == EMPTY and occupied == 0:
                    new_seat = OCCUPIED
                elif seat == OCCUPIED and occupied >= (4 + visible):
                    new_seat = EMPTY
                else:
                    new_seat = seat
                new_row.append(new_seat)
                occupied_count += new_seat == OCCUPIED
        return Grid(new_seats, occupied_count)

    def find_occupied_adjacent(self, i: int, j: int) -> int:
        count = 0
        for j_ in (j-1, j, j+1):
            for i_ in (i-1, i, i+1):
                if not (i == i_ and j == j_):
                    count += self.get_seat(i_, j_) == OCCUPIED
        return count

    def find_occupied_visible(self, i: int, j: int) -> int:
        count = 0
        for dj in (-1, 0, 1):
            for di in (-1, 0, 1):
                if di == 0 and dj == 0:
                    continue
                scalar = 1
                target = self.get_seat(i + di * scalar, j + dj * scalar)
                while target == FLOOR:
                    scalar += 1
                    target = self.get_seat(i + di * scalar, j + dj * scalar)
                count += target == OCCUPIED
        return count

    def get_seat(self, i: int, j: int) -> Optional[str]:
        if 0 <= i < len(self.seats[0]) and 0 <= j < len(self.seats):
            seat = self.seats[j][i]
        else:
            seat = None
        return seat


if __name__ == '__main__':
    main()
