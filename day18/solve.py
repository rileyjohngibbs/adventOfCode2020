import re
import sys
import time
from typing import Iterable, List, Optional, Set, Tuple, Union


def main(*args):
    input_ = load_input('test' in args)
    start = time.time()
    print(part1(input_, 'test' in args))
    mid = time.time()
    print(f'Part 1 time: {mid - start}')
    print(part2(input_, 'test' in args))
    end = time.time()
    print(f'Part 2 time: {end - mid}')


def load_input(test: bool = False) -> List[str]:
    filename = f'{"test" * test}input.txt'
    with open(filename) as f:
        return [r.strip() for r in f.readlines()]


def part1(input_: List[str], test: bool = False) -> int:
    return sum(compute_string(expression) for expression in input_)


def compute_string(expression: str) -> int:
    values: List[List[Union[int, Optional[str]]]] = [[0, '+']]
    current_value: List[int, str] = values[-1]
    for token in tokens(expression):
        if token.isdigit():
            complete_value(values[-1], int(token))
        elif token in ('+', '*'):
            values[-1][1] = token
        elif token == '(':
            values.append([0, '+'])
        elif token == ')':
            new_value = values.pop()[0]
            complete_value(values[-1], new_value)
    return values[-1][0]


def tokens(expression: str) -> str:
    next_token = ''
    for char in expression:
        if char == ' ':
            if next_token:
                yield next_token
            next_token = ''
        elif char in ('(', ')') or next_token in ('(', ')'):
            if next_token:
                yield next_token
            next_token = char
        else:
            next_token += char
    yield next_token


def complete_value(value: List[Union[int, Optional[str]]], operand: int) -> None:
    value[0] = compute_operation(*value, operand)
    value[1] = None


def compute_operation(left: int, op: str, right: int) -> int:
    if op == '+':
        return left + right
    elif op == '*':
        return left * right
    else:
        raise ValueError()


def part2(input_: List[str], test: bool = False) -> int:
    return sum(compute_string_two(expr) for expr in input_)


def compute_string_two(expression: str) -> int:
    if re.match(f'\d+ \+ \d+$', expression) is not None:
        return eval(expression)
    parens = re.match(r'.*?\(([^\(]+?)\)', expression)
    while parens is not None:
        grouping = parens.group(1)
        expression = expression.replace(
            f'({grouping})',
            str(compute_string_two(grouping)),
            1,
        )
        parens = re.match(r'.*?\(([^\(]+?)\)', expression)
    add = re.match(r'.*?(\d+ \+ \d+)', expression)
    while add is not None:
        grouping = add.group(1)
        expression = expression.replace(
            grouping,
            str(compute_string_two(grouping)),
            1,
        )
        add = re.match(r'.*?(\d+ \+ \d+)', expression)
    return eval(expression)


if __name__ == '__main__':
    main(*sys.argv)
