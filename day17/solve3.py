from enum import Enum
import numpy as np
import sys
import time
from typing import Iterable, Set, Tuple


class CubeStatus(Enum):
    INACTIVE = '.'
    ACTIVE = '#'


def main(*args):
    input_ = load_input('test' in args)
    start = time.time()
    print(part1(input_, 'test' in args))
    mid = time.time()
    print(f'Part 1 time: {mid - start}')
    print(part2(input_, 'test' in args))
    end = time.time()
    print(f'Part 2 time: {end - mid}')


def load_input(test: bool = False) -> str:
    filename = f'{"test" * test}input.txt'
    with open(filename) as f:
        return f.read()


Vector = Tuple[int, ...]


class Space:

    CYCLES = 6
    ACTIVE_CHAR = '#'
    DIMENSIONS = 3

    array: np.ndarray

    def __init__(self, input_: str):
        cubes = [
            [v == self.ACTIVE_CHAR for v in row]
            for row in input_.split('\n')
            if row
        ]
        ys = len(cubes) + 2 * (self.CYCLES + 1)
        xs = len(cubes[0]) + 2 * (self.CYCLES + 1)
        zs = 1 + 2 * (self.CYCLES + 1)
        self.array = np.zeros((zs, ys, xs), dtype=bool)
        self.array[
            self.CYCLES + 1,
            self.CYCLES + 1:self.CYCLES + len(cubes) + 1,
            self.CYCLES + 1:self.CYCLES + len(cubes[0]) + 1,
        ] = cubes

    def __str__(self) -> str:
        mesh_components = []
        for d in range(self.DIMENSIONS):
            box = self.array
            for n in range(self.DIMENSIONS - 1, -1, -1):
                if n == d:
                    continue
                box = box.any(n)
            nonzeros = box.nonzero()[0]
            mesh_components.append(range(nonzeros.min(), nonzeros.max() + 1))
        mesh = np.ix_(*mesh_components)
        return str(self.array[mesh])

    @property
    def active_cubes(self) -> Tuple[np.ndarray]:
        return np.transpose(self.array.nonzero())

    def get_neighborhood(self, address: np.ndarray) -> np.ndarray:
        mesh = np.ix_(*np.transpose((address - 1, address, address + 1)))
        return self.array[mesh]

    def neighborhood_active(self, address: np.ndarray) -> int:
        return self.get_neighborhood(address).sum() - self.array[tuple(address)]

    def neighborhood_inactive_addresses(
            self,
            address: np.ndarray,
    ) -> np.ndarray:
        neighborhood = self.get_neighborhood(address)
        relative_addresses = np.transpose((~neighborhood).nonzero())
        return relative_addresses + address - 1

    def cycle(self) -> None:
        checked: Set[Vector] = set()
        to_flip: Set[Vector] = set()
        for cube_address in self.active_cubes:
            if self.should_flip(cube_address):
                to_flip.add(tuple(cube_address))
            checked.add(tuple(cube_address))
            inactive_neighbor_addresses = self.neighborhood_inactive_addresses(
                cube_address,
            )
            for neighbor_address in inactive_neighbor_addresses:
                if tuple(neighbor_address) in checked:
                    continue
                if self.should_flip(neighbor_address):
                    to_flip.add(tuple(neighbor_address))
                checked.add(tuple(neighbor_address))
        for flipper in to_flip:
            self.array[flipper] = ~self.array[flipper]

    def should_flip(self, address: np.ndarray) -> bool:
        if self.array[tuple(address)]:
            return self.neighborhood_active(address) not in (2, 3)
        else:
            return self.neighborhood_active(address) == 3


class HyperSpace(Space):

    DIMENSIONS = 4

    def __init__(self, input_: str):
        cubes = [
            [v == self.ACTIVE_CHAR for v in row]
            for row in input_.split('\n')
            if row
        ]
        ys = len(cubes) + 2 * (self.CYCLES + 1)
        xs = len(cubes[0]) + 2 * (self.CYCLES + 1)
        zs = 1 + 2 * (self.CYCLES + 1)
        ws = 1 + 2 * (self.CYCLES + 1)
        self.array = np.zeros((ws, zs, ys, xs), dtype=bool)
        self.array[
            self.CYCLES + 1,
            self.CYCLES + 1,
            self.CYCLES + 1:self.CYCLES + len(cubes) + 1,
            self.CYCLES + 1:self.CYCLES + len(cubes[0]) + 1,
        ] = cubes


def part1(input_: str, test: bool = False) -> int:
    space = Space(input_)
    for _ in range(6):
        space.cycle()
    return len(space.active_cubes)


def part2(input_: str, test: bool = False) -> int:
    space = HyperSpace(input_)
    for _ in range(6):
        space.cycle()
    return len(space.active_cubes)


if __name__ == '__main__':
    main(*sys.argv)
