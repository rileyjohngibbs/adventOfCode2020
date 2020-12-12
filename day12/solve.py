import re
import sys
import time
from typing import List, NewType, Tuple


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


def part1(input_: List[str], test: bool = False):
    direction, location = (1, 0), (0, 0)
    for instruction in input_:
        direction, location = follow_instruction(
            direction,
            location,
            instruction,
        )
    return sum(map(abs, location))


def follow_instruction(
        direction: Tuple[int, int],
        location: Tuple[int, int],
        instruction: str,
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    move, svalue = re.match(r'(.)(\d+)', instruction).groups()
    value = int(svalue)
    if move == 'L':
        for _ in range(value // 90):
            direction = left_turn(direction)
    elif move == 'R':
        for _ in range(value // 90):
            direction = right_turn(direction)
    elif move == 'F':
        location = add_vectors(location, scale(direction, value))
    else:
        vector_factory = {
            'N': lambda v: (0, v),
            'E': lambda v: (v, 0),
            'S': lambda v: (0, -v),
            'W': lambda v: (-v, 0),
        }[move]
        location = add_vectors(location, vector_factory(value))
    return direction, location


def left_turn(direction: Tuple[int, int]) -> Tuple[int, int]:
    return (-direction[1], direction[0])


def right_turn(direction: Tuple[int, int]) -> Tuple[int, int]:
    return (direction[1], -direction[0])


def add_vectors(va: Tuple[int, int], vb: Tuple[int, int]) -> Tuple[int, int]:
    return (va[0] + vb[0], va[1] + vb[1])


def scale(vector: Tuple[int, int], scalar: int) -> Tuple[int, int]:
    return (vector[0] * scalar, vector[1] * scalar)


Vector = Tuple[int, int]
Waypoint = NewType('Waypoint', Vector)
Ship = NewType('Waypoint', Vector)


def part2(input_: List[str], test: bool = False):
    waypoint, location = (10, 1), (0, 0)
    for instruction in input_:
        waypoint, location = follow_waypoint_instruction(
            waypoint,
            location,
            instruction,
        )
    return sum(map(abs, location))


def follow_waypoint_instruction(
        waypoint: Tuple[int, int],
        location: Tuple[int, int],
        instruction: str,
) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    move, svalue = re.match(r'(.)(\d+)', instruction).groups()
    value = int(svalue)
    if move == 'L':
        for _ in range(value // 90):
            waypoint = orbit_left(waypoint)
    elif move == 'R':
        for _ in range(value // 90):
            waypoint = orbit_right(waypoint)
    elif move == 'F':
        location = move_to_waypoint(location, waypoint, value)
    else:
        vector_factory = {
            'N': lambda v: (0, v),
            'E': lambda v: (v, 0),
            'S': lambda v: (0, -v),
            'W': lambda v: (-v, 0),
        }[move]
        waypoint = add_vectors(waypoint, vector_factory(value))
    return waypoint, location


def orbit_left(waypoint: Waypoint) -> Waypoint:
    return left_turn(waypoint)


def orbit_right(waypoint: Waypoint) -> Waypoint:
    return right_turn(waypoint)


def move_to_waypoint(location: Ship, waypoint: Waypoint, number: int) -> Ship:
    return add_vectors(location, scale(waypoint, number))


if __name__ == '__main__':
    main(*sys.argv)
