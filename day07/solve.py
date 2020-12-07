import re
from typing import Dict, List, Tuple

Tree = Dict[str, Dict[str, int]]
# {'red': {'blue': 5, 'green': 1}}


def main():
    input_ = load_input()
    print(part1(input_))
    print(part2(input_))


def load_input():
    with open('input.txt') as f:
        return [r.strip() for r in f.readlines()]


def part1(input_: list):
    parents, children = parse_rules(input_)
    outers = set()
    current = set(parents['shiny gold'])
    while current:
        outers.update(current)
        current = {p for c in current for p in parents.get(c, {})}
    return len(outers)


def part2(input_: list):
    parents, children = parse_rules(input_)
    return get_children_count('shiny gold', 1, children) - 1


def get_children_count(parent: str, parent_count: int, child_dict: dict) -> int:
    children = child_dict.get(parent)
    if children is None:
        return parent_count
    else:
        return sum(
            get_children_count(
                child, parent_count * child_count, child_dict,
            )
            for child, child_count in children.items()
        ) + parent_count


def parse_rules(input_: List[str]) -> Tuple[Tree, Tree]:
    parents = {}
    children = {}
    for rule in input_:
        m = re.match(r'(?P<outer>.*) bags contain (?P<inners>.*).', rule)
        outer = m.group('outer')
        inners_raw = m.group('inners').split(', ')
        for i in inners_raw:
            if 'no other bags' in i:
                continue
            count, inner = re.match(r'(\d+) (.*) bags?', i).groups()
            children.setdefault(outer, {})[inner] = int(count)
            parents.setdefault(inner, {})[outer] = int(count)
    return parents, children


if __name__ == '__main__':
    main()
