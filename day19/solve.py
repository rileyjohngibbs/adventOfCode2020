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


def load_input(test: bool = False) -> Tuple[List[str], List[str]]:
    filename = f'{"test" * test}input.txt'
    with open(filename) as f:
        return tuple(
            [r for r in section.split('\n') if r]
            for section in f.read().split('\n\n')
        )


def part1(input_: Tuple[List[str], List[str]], test: bool = False) -> int:
    unparsed_rules, messages = input_
    rules = dict(RuleSet.parse_rule(pr) for pr in unparsed_rules)
    regex = re.compile(RuleSet(rules).emit(0) + '$')
    if test:
        print(regex)
    return sum(1 for m in messages if regex.match(m) is not None)


def part2(input_: Tuple[List[str], List[str]], test: bool = False) -> int:
    # Doesn't work
    unparsed_rules, messages = input_
    rules = dict(RuleSet.parse_rule(pr) for pr in unparsed_rules)
    regex = re.compile(RuleSet(rules, True).emit(0) + '$')
    if test:
        print(regex)
    return sum(1 for m in messages if regex.match(m) is not None)


class RuleSet:

    rules: dict
    part2: bool

    def __init__(self, rules: dict, part2: bool = False):
        self.rules = rules
        self.part2 = part2

    @staticmethod
    def parse_rule(rule: str) -> Tuple[int, List[List[Union[int, str]]]]:
        index, definition = rule.split(': ')
        if definition in ('"a"', '"b"'):
            productions = [[definition[1]]]
        else:
            productions = [
                [int(i) for i in piece.split(' ')]
                for piece in definition.split(' | ')
            ]
        return int(index), productions

    def emit(self, rule: Union[str, int]) -> str:
        if type(rule) == str:
            return rule
        productions = self.rules[rule]
        if self.part2 and rule == 8:
            return '(' + self.emit(42) + ')+'
        if self.part2 and rule == 11:
            return f'(({self.emit(42)})+({self.emit(31)})+)'
        return '(' + '|'.join(
            ''.join(self.emit(r) for r in p)
            for p in productions
        ) + ')'


if __name__ == '__main__':
    main(*sys.argv)
