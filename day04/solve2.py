import re


def main():
    passports = parse_input(load_input())
    print(part1(passports))
    print(part2(passports))


OPTIONAL_FIELDS = {'cid'}

VALIDATORS = {
    'byr': lambda s: 1920 <= int(re.match(r'\d{4}$', s) and s) <= 2002,
    'iyr': lambda s: len(s) == 4 and s.isdigit() and 2010 <= int(s) <= 2020,
    'eyr': lambda s: len(s) == 4 and s.isdigit() and 2020 <= int(s) <= 2030,
    'hgt': lambda s: s[:-2].isdigit() and (
        150 <= int(s[:-2]) <= 193 if s[-2:] == 'cm'
        else 59 <= int(s[:-2]) <= 76 if s[-2:] == 'in'
        else False
    ),
    'hcl': lambda s: re.match(r'#[0-9a-f]{6}$', s) is not None,
    'ecl': lambda s: s in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
    'pid': lambda s: len(s) == 9 and s.isdigit(),
}


class PassportValidator:

    passport: dict

    def __init__(self, passport: dict):
        self.passport = passport

    def byr(self) -> bool:
        value = self.passport.get('byr')
        return (
            value is not None
            and 1920 <= int(re.match(r'\d{4}$', value) and value) <= 2002
        )

def load_input():
    with open('input.txt') as f:
        return f.read()


def parse_input(input_: str):
    passports = [
        dict([
            re.match(r'(.*):(.*)', v).groups()
            for v in p.split()
        ])
        for p in input_.split('\n\n')
    ]
    return passports


def part1(passports: list) -> int:
    return len([
        passport for passport in passports
        if set(VALIDATORS) - set(passport) == set()
    ])


def part2(passports: list) -> int:
    return len([
        passport for passport in passports
        if all(
            field_name in passport
            and VALIDATORS[field_name](passport[field_name])
            for field_name in VALIDATORS
        )
    ])
    return count


if __name__ == '__main__':
    main()
