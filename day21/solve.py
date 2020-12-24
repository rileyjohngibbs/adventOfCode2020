import re
import sys
import time
from typing import Iterable, List, Optional, Set, Tuple, Union


def main(*args):
    start = time.time()
    input_ = load_input('test' in args)
    print(part1(input_, 'test' in args))
    mid = time.time()
    input_ = load_input('test' in args)
    print(f'Part 1 time: {mid - start}')
    print(part2(input_, 'test' in args))
    end = time.time()
    print(f'Part 2 time: {end - mid}')


def load_input(test: bool = False) -> List[str]:
    filename = f'{"test" * test}input.txt'
    with open(filename) as f:
        return [r.strip() for r in f.readlines() if r]


def part1(input_: List[str], test: bool = False) -> int:
    potential_sources: Dict[str, Set[str]] = {}
    all_ingredients: Set[str] = set()
    for ingredient_list in input_:
        ingredients, allergens = parse_ingredients(ingredient_list)
        for allergen in allergens:
            potential_sources.setdefault(
                allergen, set(ingredients),
            ).intersection_update(ingredients)
        all_ingredients.update(ingredients)
    solved_allergens: Set[str] = set()
    changed = True
    while changed:
        changed = False
        for allergen in filter(
            lambda a: a not in solved_allergens
                and len(potential_sources[a]) == 1,
            potential_sources,
        ):
            changed = True
            solved_allergens.add(allergen)
            ingredient = next(a for a in potential_sources[allergen])
            for a, sources in potential_sources.items():
                if a != allergen and ingredient in sources:
                    sources.remove(ingredient)
    no_allergens = all_ingredients - set.union(set(), *potential_sources.values())
    return sum(
        1
        for ingr in no_allergens
        for il in input_
        if ingr in il.split()
    )


def part2(input_: List[List[int]], test: bool = False) -> int:
    potential_sources: Dict[str, Set[str]] = {}
    all_ingredients: Set[str] = set()
    for ingredient_list in input_:
        ingredients, allergens = parse_ingredients(ingredient_list)
        for allergen in allergens:
            potential_sources.setdefault(
                allergen, set(ingredients),
            ).intersection_update(ingredients)
        all_ingredients.update(ingredients)
    solved_allergens: Set[str] = set()
    changed = True
    while changed:
        changed = False
        for allergen in filter(
            lambda a: a not in solved_allergens
                and len(potential_sources[a]) == 1,
            potential_sources,
        ):
            changed = True
            solved_allergens.add(allergen)
            ingredient = next(a for a in potential_sources[allergen])
            for a, sources in potential_sources.items():
                if a != allergen and ingredient in sources:
                    sources.remove(ingredient)
    return ','.join(
        ingredient
        for allergen, ingredient_set in sorted(
            potential_sources.items(),
            key=lambda item: item[0],
        )
        for ingredient in ingredient_set
    )


def parse_ingredients(raw_ingredients: str) -> Tuple[List[str], List[str]]:
    match = re.match(r'(.*?)(?:\(contains (.*)\))?$', raw_ingredients)
    ingredients = match.group(1).split()
    allergens = match.group(2) and match.group(2).split(', ') or []
    return ingredients, allergens


if __name__ == '__main__':
    main(*sys.argv)
