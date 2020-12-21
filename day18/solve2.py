from functools import reduce
import sys
import time
from typing import Iterable, List, Optional, Set, Tuple, Union

from compiler import RuleSet


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
    rule_set = RuleSet()

    rule_set.add_token('Num', '1234567890', lambda self: int(self.value))
    rule_set.add_token('MultSign', '*', None)
    rule_set.add_token('AddSign', '+', None)
    rule_set.add_token('LParen', '(', None)
    rule_set.add_token('RParen', ')', None)

    rule_set.add_rule(
        'Comp',
        [['Value', 'CompTail']],
        lambda self: self.production[1].emit()(self.production[0].emit())
    )

    def tail_emit(self):
        if self.null:
            return lambda x: x
        else:
            right = self.production[1].emit()
            tail_operation = self.production[2].emit()
            if type(self.production[0]).__name__ == 'MultSign':
                return lambda left: tail_operation(left * right)
            else:
                return lambda left: tail_operation(left + right)
    rule_set.add_rule(
        'CompTail',
        [['MultSign', 'Value', 'CompTail'], ['AddSign', 'Value', 'CompTail']],
        tail_emit,
        nullable=True,
    )
    rule_set.add_rule(
        'Value',
        [['Num'], ['LParen', 'Comp', 'RParen']],
        lambda self: (
            self.production[0].emit()
            if type(self.production[0]).__name__ == 'Num'
            else self.production[1].emit()
        ),
    )

    return sum(
        rule_set.compile((c for c in computation if c != ' '), 'Comp')
        for computation in input_
    )


def part2(input_: List[str], test: bool = False) -> int:
    rule_set = RuleSet()

    rule_set.add_token('Num', '1234567890', lambda self: int(self.value))
    rule_set.add_token('MultSign', '*', None)
    rule_set.add_token('AddSign', '+', None)
    rule_set.add_token('LParen', '(', None)
    rule_set.add_token('RParen', ')', None)

    rule_set.add_rule(
        'Mult',
        [['Add', 'MultTail']],
        lambda self: reduce(
            lambda a, b: a * b,
            (rule.emit() for rule in self.production),
        ),
    )
    rule_set.add_rule(
        'MultTail',
        [['MultSign', 'Add', 'MultTail']],
        lambda self: self.null or reduce(
            lambda a, b: a * b,
            (rule.emit() for rule in self.production[1:]),
        ),
        nullable=True,
    )
    rule_set.add_rule(
        'Add',
        [['Value', 'AddTail']],
        lambda self: sum(rule.emit() for rule in self.production),
    )
    rule_set.add_rule(
        'AddTail',
        [['AddSign', 'Value', 'AddTail']],
        lambda self: 0 if self.null else sum(
            rule.emit() for rule in self.production[1:]
        ),
        nullable=True,
    )
    rule_set.add_rule(
        'Value',
        [['Num'], ['LParen', 'Mult', 'RParen']],
        lambda self: (
            self.production[0].emit()
            if type(self.production[0]).__name__ == 'Num'
            else self.production[1].emit()
        ),
    )

    return sum(
        rule_set.compile((c for c in computation if c != ' '), 'Mult')
        for computation in input_
    )


if __name__ == '__main__':
    main(*sys.argv)
