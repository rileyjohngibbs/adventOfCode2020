from enum import Enum
from typing import Iterator, List, Optional, TypeVar

class SeatValue(Enum):
    FLOOR = '.'
    OCCUPIED = '#'
    EMPTY = 'L'


def main():
    input_ = load_input()
    print(part1(input_))
    print(part2(input_))


def load_input() -> List[int]:
    with open('input.txt') as f:
        return [r.strip() for r in f.readlines()]


S = TypeVar('S', bound='Seat')


class Seat:

    value: SeatValue
    static: bool
    static_neighbors: list
    active_neighbors: list
    static_neighbors_occupied: int

    def __init__(self, value: str):
        self.value = SeatValue(value)
        self.static = self.value is SeatValue.FLOOR
        self.static_neighbors = []
        self.active_neighbors = []
        self.static_neighbors_occupied = 0

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
            )
            or self.max_occupied_neighbors < 4
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


class Grid:

    seat_grid: List[List[Seat]]
    height: int
    width: int

    def __init__(self, input_: List[List[str]]):
        self.seat_grid = [[Seat(value) for value in row] for row in input_]
        self.height = len(self.seat_grid)
        self.width = len(self.seat_grid[0])
        for j, row in enumerate(input_):
            for i, value in enumerate(row):
                seat = self.get_seat(j, i)
                for neighbor in self.get_neighbors(j, i):
                    seat.add_neighbor(neighbor)

    @property
    def seats(self) -> Iterator[Seat]:
        return (seat for row in self.seat_grid for seat in row)

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


def part1(input_: List[str]) -> int:
    pass


def part2(input_: List[str]) -> int:
    pass
