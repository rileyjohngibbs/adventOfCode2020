import re
from validator import Field, Validator


def main():
    passports = parse_input(load_input())
    print(part1(passports))
    print(part2(passports))


class PassportValidator(Validator):

    byr = Field(length=4, in_=(1920, 2002))
    iyr = Field(length=4, in_=(2010, 2020))
    eyr = Field(length=4, in_=(2020, 2030))
    hgt = Field(name='hgt', regex=(
        r'(\d+)(cm|in)',
        lambda height, unit: (
            150 <= int(height) <= 193
            if unit == 'cm'
            else 59 <= int(height) <= 76
        )
    ))
    hcl = Field(name='hcl', regex=(r'#[0-9a-f]{6}$',))
    ecl = Field(name='ecl', regex=(r'amb|blu|brn|gry|grn|hzl|oth',))
    pid = Field(name='pid', regex=(r'\d{9}$',))

    def __init__(self, passport):
        self.passport = passport


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
        if set(PassportValidator._required) - set(passport) == set()
    ])


def part2(passports: list) -> int:
    return len([
        passport for passport in passports
        if PassportValidator(passport).validate()
    ])
    return count


if __name__ == '__main__':
    main()
