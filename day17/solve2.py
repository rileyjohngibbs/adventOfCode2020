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


def load_input(test: bool = False) -> str:
    filename = f'{"test" * test}input.txt'
    with open(filename) as f:
        return f.read()


Vector = Tuple[int, ...]


class Space:

    NEIGHBOR_VECTORS: Tuple[Vector, ...] = tuple(
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

    def get_neighbor_addresses(
            self,
            vector: Vector,
    ) -> Tuple[List[Vector], List[Vector]]:
        active: List[Vector] = []
        inactive: List[Vector] = []
        for nvector in self.NEIGHBOR_VECTORS:
            address = tuple(map(sum, zip(vector, nvector)))
            if address in self.active_cubes:
                active.append(address)
            else:
                inactive.append(address)
        return active, inactive

    def cycle(self) -> None:
        checked: Set[Vector] = set()
        to_deactivate: List[Vector] = []
        to_activate: List[Vector] = []
        for cube_address in self.active_cubes:
            active, inactive = self.get_neighbor_addresses(cube_address)
            if self.should_flip(cube_address, active, True):
                to_deactivate.append(cube_address)
            checked.add(cube_address)
            for neighbor in inactive:
                if neighbor in checked:
                    continue
                meta_active, _ = self.get_neighbor_addresses(neighbor)
                if self.should_flip(neighbor, meta_active, False):
                    to_activate.append(neighbor)
                checked.add(neighbor)
        for flipper in to_deactivate:
            self.active_cubes.remove(flipper)
        for flipper in to_activate:
            self.active_cubes.add(flipper)

    def should_flip(
            self,
            cube: Vector,
            active_neighbors: Iterable[Vector],
            is_active: bool,
    ) -> bool:
        active_count = len(active_neighbors)
        return (
            is_active and active_count not in (2, 3)
            or not is_active and active_count == 3
        )


class HyperSpace(Space):

    NEIGHBOR_VECTORS: Tuple[Vector, ...] = tuple(
        (x, y, z, w)
        for z in range(-1, 2)
        for y in range(-1, 2)
        for x in range(-1, 2)
        for w in range(-1, 2)
        if (x, y, z, w) != (0, 0, 0, 0)
    )

    def __init__(self, input_: str):
        cubes = [
            [CubeStatus(v) for v in row]
            for row in input_.split('\n')
            if row
        ]
        self.active_cubes = {
            (x, y, 0, 0)
            for y, row in enumerate(cubes)
            for x, cube in enumerate(row)
            if cube is CubeStatus.ACTIVE
        }


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
