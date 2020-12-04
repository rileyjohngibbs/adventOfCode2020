import re


REQUIRED_FIELDS = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
OPTIONAL_FIELDS = {'cid'}

VALIDATION = {
    'byr': lambda s: len(s) == 4 and s.isdigit() and 1920 <= int(s) <= 2002,
    'iyr': lambda s: len(s) == 4 and s.isdigit() and 2010 <= int(s) <= 2020,
    'eyr': lambda s: len(s) == 4 and s.isdigit() and 2020 <= int(s) <= 2030,
    'hgt': lambda s: s[:-2].isdigit() and (
        150 <= int(s[:-2]) <= 193 if s[-2:] == 'cm'
        else 59 <= int(s[:-2]) <= 76 if s[-2:] == 'in'
        else False
    ),
    'hcl': lambda s: len(s) == 7 and s[0] == '#' and all(
        c in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')
        for c in s[1:]
    ),
    'ecl': lambda s: s in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
    'pid': lambda s: len(s) == 9 and s.isdigit(),
}


def load_input():
    with open('input.txt') as f:
        return f.read()


def parse_input(input_: str):
    passports = [p.split() for p in input_.split('\n\n')]
    return passports


def main():
    passports = parse_input(load_input())
    print(part1(passports))
    print(part2(passports))


def part1(passports: list) -> int:
    count = 0
    for passport in passports:
        fields = set(f[:3] for f in passport)
        if REQUIRED_FIELDS - fields == set():
            count += 1
    return count


def part2(passports: list) -> int:
    count = 0
    for passport in passports:
        values = {f.split(':')[0]: f.split(':')[1] for f in passport}
        if all(
            k in values and VALIDATION[k](values[k])
            for k in VALIDATION
        ):
            count += 1
    return count


if __name__ == '__main__':
    main()
