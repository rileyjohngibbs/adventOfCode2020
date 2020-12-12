from enum import Enum
import sys
import time
from typing import Iterator, List, Optional, Set, TypeVar

class SeatValue(Enum):
    FLOOR = '.'
    OCCUPIED = '#'
    EMPTY = 'L'


def main(*args):
    input_ = load_input('test' in args)
    start = time.time()
    print(part1(input_, 'test' in args))
    mid = time.time()
    print(f'Part 1 time: {mid - start}')
    print(part2(input_, 'test' in args))
    end = time.time()
    print(f'Part 2 time: {end - mid}')


def load_input(test: bool = False) -> List[int]:
    filename = f'{"test" * test}input.txt'
    with open(filename) as f:
        return [r.strip() for r in f.readlines()]


S = TypeVar('S', bound='Seat')


class Seat:

    value: SeatValue
    static: bool
    static_neighbors: list
    active_neighbors: list
    static_neighbors_occupied: int
    threshold: int

    def __init__(self, value: str, threshold: int):
        self.value = SeatValue(value)
        self.static = self.value is SeatValue.FLOOR
        self.static_neighbors = []
        self.active_neighbors = []
        self.static_neighbors_occupied = 0
        self.threshold = threshold

    def __repr__(self) -> str:
        return f'<Seat: {self.value}>'

    def add_neighbor(self, neighbor: S) -> None:
        if neighbor.static:
            self.static_neighbors.append(neighbor)
            self.static_neighbors_occupied += (
                neighbor.value is SeatValue.OCCUPIED
            )
        else:
            self.active_neighbors.append(neighbor)

    def update_static_status(self) -> None:
        still_active = []
        for neighbor in self.active_neighbors:
            if neighbor.static:
                self.static_neighbors.append(neighbor)
                self.static_neighbors_occupied += (
                    neighbor.value is SeatValue.OCCUPIED
                )
            else:
                still_active.append(neighbor)
        self.active_neighbors = still_active
        self.static = (
            self.value is SeatValue.FLOOR
            or (
                self.value is SeatValue.EMPTY
                and self.static_neighbors_occupied > 0
            ) or (
                self.value is SeatValue.OCCUPIED
                and self.max_occupied_neighbors < self.threshold
            )
        )

    @property
    def max_occupied_neighbors(self) -> int:
        return len(self.active_neighbors) + self.static_neighbors_occupied

    @property
    def neighbors(self) -> List:
        return self.active_neighbors + self.static_neighbors

    def flip(self) -> None:
        if self.value is SeatValue.OCCUPIED:
            self.value = SeatValue.EMPTY
        elif self.value is SeatValue.EMPTY:
            self.value = SeatValue.OCCUPIED
        else:
            raise ValueError(f'Seat is {self.value} and should not be flipped')

    def check_for_flip_anticipation(self) -> bool:
        self.update_static_status()
        return not self.static and (
            (
                self.value is SeatValue.EMPTY
                and self.occupied_neighbors_count == 0
            ) or (
                self.value is SeatValue.OCCUPIED
                and self.occupied_neighbors_count >= self.threshold
            )
        )

    @property
    def occupied_neighbors_count(self) -> int:
        return self.static_neighbors_occupied + sum(
            neighbor.value is SeatValue.OCCUPIED
            for neighbor in self.active_neighbors
        )


class Grid:

    THRESHOLD = 4

    seat_grid: List[List[Seat]]
    height: int
    width: int
    active_seats: Set[Seat]

    def __init__(self, input_: List[List[str]]):
        self.seat_grid = [
            [Seat(value, self.THRESHOLD) for value in row]
            for row in input_
        ]
        self.height = len(self.seat_grid)
        self.width = len(self.seat_grid[0])
        for j, row in enumerate(input_):
            for i, value in enumerate(row):
                seat = self.get_seat(j, i)
                for neighbor in self.get_neighbors(j, i):
                    seat.add_neighbor(neighbor)
        self.active_seats = set(self.seats)

    def __str__(self) -> str:
        return '\n'.join(
            ''.join(seat.value.value for seat in row)
            for row in self.seat_grid
        )

    @property
    def seats(self) -> Iterator[Seat]:
        return (seat for row in self.seat_grid for seat in row)

    def update_active_seats(self) -> None:
        self.active_seats = [
            seat for seat in self.active_seats
            if seat.static is False
        ]

    def get_seat(self, row: int, col: int) -> Optional[Seat]:
        if 0 <= row < self.height and 0 <= col < self.width:
            seat = self.seat_grid[row][col]
        else:
            seat = None
        return seat

    def get_neighbors(self, row: int, col: int) -> List[Seat]:
        return list(filter(None, (
            self.get_seat(row + dr, col + dc)
            for dr, dc in (
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 1),
                (1, -1), (1, 0), (1, 1),
            )
        )))

    def iterate(self) -> None:
        flippers, still_active = [], set()
        for seat in self.active_seats:
            if seat.check_for_flip_anticipation():
                flippers.append(seat)
            if not seat.static:
                still_active.add(seat)
        for seat in flippers:
            seat.flip()
        self.active_seats = still_active


class GridTwo(Grid):

    THRESHOLD = 5

    def get_neighbors(self, row: int, col: int) -> List[Seat]:
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        neighbors = []
        for dr, dc in directions:
            vector = (row + dr, col + dc)
            neighbor = self.get_seat(*vector)
            while neighbor and neighbor.value is SeatValue.FLOOR:
                vector = (vector[0] + dr, vector[1] + dc)
                neighbor = self.get_seat(*vector)
            if neighbor is not None:
                neighbors.append(neighbor)
        return neighbors


def part1(input_: List[str], test: bool = False) -> int:
    grid = Grid(input_)
    if test:
        print(grid)
        print('-'*grid.width)
    while grid.active_seats:
        grid.iterate()
        if test:
            print(grid)
            print('-'*grid.width)
    return sum(int(seat.value is SeatValue.OCCUPIED) for seat in grid.seats)


def part2(input_: List[str], test: bool = False) -> int:
    grid = GridTwo(input_)
    if test:
        print(grid)
        print('-'*grid.width)
    while grid.active_seats:
        grid.iterate()
        if test:
            print(grid)
            print('-'*grid.width)
    return sum(int(seat.value is SeatValue.OCCUPIED) for seat in grid.seats)


if __name__ == '__main__':
    main(*sys.argv)
