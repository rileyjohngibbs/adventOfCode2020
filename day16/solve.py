from functools import reduce
import numpy as np
import re
import sys
import time
from typing import Dict, List, Optional, Tuple

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
        contents = f.read().strip()
    return contents.split('\n\n')


class Rule:

    name: str
    min_1: int
    max_1: int
    min_2: int
    max_2: int

    def __init__(
        self, name: str, min_1: int, max_1: int, min_2: int, max_2: int,
    ):
        self.name = name
        self.min_1 = min_1
        self.max_1 = max_1
        self.min_2 = min_2
        self.max_2 = max_2

    def validate_vector(self, vector: np.ndarray) -> np.ndarray:
        return (
            (vector >= self.min_1) * (vector <= self.max_1)
            + (vector >= self.min_2) * (vector <= self.max_2)
        )


def parse_input(
        input_: List[str]
) -> Tuple[List[Rule], List[int], List[List[int]]]:
    raw_rules, raw_my_ticket, raw_tickets = input_
    rules = [parse_rule(rr) for rr in raw_rules.split('\n')]
    my_ticket = [int(v) for v in raw_my_ticket.split('\n')[1].split(',')]
    tickets = [[int(v) for v in t.split(',')] for t in raw_tickets.split('\n')[1:]]
    return rules, my_ticket, tickets


def parse_rule(rule: str) -> Rule:
    match = re.match(r'(.*): (\d+)-(\d+) or (\d+)-(\d+)', rule)
    return Rule(match.group(1), *map(int, match.groups()[1:]))


def part1(input_: List[str], test: bool = False) -> int:
    rules, my_ticket, tickets = parse_input(input_)
    error_rate = 0
    for ticket in tickets:
        matrix = np.empty((len(ticket), len(rules)), dtype=int)
        for i, value in enumerate(ticket):
            matrix[i].fill(value)
        for j, rule in enumerate(rules):
            matrix[:,j] = rule.validate_vector(matrix[:,j])
        bad_indices = (matrix.any(1) - 1).nonzero()[0]
        for index in bad_indices:
            error_rate += ticket[index]
    return error_rate


def part2(input_: List[int], test: bool = False) -> int:
    rules, my_ticket, tickets = parse_input(input_)
    valid_tickets = []
    for ticket in tickets:
        matrix = np.empty((len(ticket), len(rules)), dtype=int)
        for i, value in enumerate(ticket):
            matrix[i].fill(value)
        for j, rule in enumerate(rules):
            matrix[:,j] = rule.validate_vector(matrix[:,j])
        bad_indices = (matrix.any(1) - 1).nonzero()[0]
        if len(bad_indices) == 0:
            valid_tickets.append(matrix)
    super_matrix = np.array(valid_tickets)
    solution_space = super_matrix.all(0)
    solution = search_for_solution(solution_space)
    key = 'departure' if not test else 's'
    ticket_values = (
        my_ticket[solution[:,col].nonzero()[0][0]]
        for col, rule in enumerate(rules)
        if key in rule.name
    )
    departure_product = reduce(lambda a, b: a * b, ticket_values, 1)
    return departure_product


def search_for_solution(matrix: np.ndarray) -> Optional[np.ndarray]:
    valid_field_counts = matrix.sum(0)
    if not valid_field_counts.all():
        return None
    elif (valid_field_counts == 1).all():
        return matrix
    else:
        matrix_copy = matrix.copy()
        singleton_rules = [
            col for col in (valid_field_counts == 1).nonzero()[0]
            if matrix[matrix[:,col].nonzero()[0][0]].sum() > 1
        ]
        if len(singleton_rules) == 0:
            return None
        for col in (valid_field_counts == 1).nonzero()[0]:
            row = matrix[:,col].nonzero()[0][0]
            matrix_copy[row].fill(False)
            matrix_copy[row,col] = True
        return search_for_solution(matrix_copy)


if __name__ == '__main__':
    main(*sys.argv)
