from enum import Enum
import sys
import time
from typing import Iterable, List, Set, Tuple

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


def load_input(test: bool = False) -> List[int]:
    filename = f'{"test" * test}input.txt'
    with open(filename) as f:
        return f.read()


Vector = Tuple[int, ...]


class Space:

    NEIGHBOR_VECTORS: Tuple[Vector] = tuple(
        (x, y, z)
        for z in range(-1, 2)
        for y in range(-1, 2)
        for x in range(-1, 2)
        if (x, y, z) != (0, 0, 0)
    )

    active_cubes: Set[Vector]

    def __init__(self, input_: str):
        cubes = [
            [CubeStatus(v) for v in row]
            for row in input_.split('\n')
            if row
        ]
        self.active_cubes = set()
        for y, row in enumerate(cubes):
            for x, cube in enumerate(row):
                if cube is CubeStatus.ACTIVE:
                    self.active_cubes.add((x, y, 0))

    def get_neighbor_addresses(self, vector: Vector) -> Set[Vector]:
        return {
            tuple(map(sum, zip(vector, nvector)))
            for nvector in self.NEIGHBOR_VECTORS
        }

    def cycle(self) -> None:
        checked: Set[Vector] = set()
        to_flip: Set[Vector] = set()
        for cube_address in self.active_cubes:
            neighbors = self.get_neighbor_addresses(cube_address)
            if self.should_flip(cube_address, neighbors):
                to_flip.add(cube_address)
            checked.add(cube_address)
            inactive_neighbors = (
                n for n in neighbors
                if n not in self.active_cubes
                and n not in checked
            )
            for neighbor in inactive_neighbors:
                neighbor_neighbors = self.get_neighbor_addresses(neighbor)
                if self.should_flip(neighbor, neighbor_neighbors):
                    to_flip.add(neighbor)
                checked.add(neighbor)
        for flipper in to_flip:
            if flipper in self.active_cubes:
                self.active_cubes.remove(flipper)
            else:
                self.active_cubes.add(flipper)

    def should_flip(self, cube: Vector, neighbors: Iterable[Vector]) -> bool:
        active_count = len([n for n in neighbors if n in self.active_cubes])
        return (
            cube in self.active_cubes and active_count not in (2, 3)
            or cube not in self.active_cubes and active_count == 3
        )


class HyperSpace(Space):

    NEIGHBOR_VECTORS: Tuple[Vector] = tuple(
        (x, y, z, w)
        for z in range(-1, 2)
        for y in range(-1, 2)
        for x in range(-1, 2)
        for w in range(-1, 2)
        if (x, y, z, w) != (0, 0, 0, 0)
    )

    active_cubes: Set[Vector]

    def __init__(self, input_: str):
        cubes = [
            [CubeStatus(v) for v in row]
            for row in input_.split('\n')
            if row
        ]
        self.active_cubes = set()
        for y, row in enumerate(cubes):
            for x, cube in enumerate(row):
                if cube is CubeStatus.ACTIVE:
                    self.active_cubes.add((x, y, 0, 0))


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
