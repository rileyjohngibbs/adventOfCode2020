import re


def main():
    passports = parse_input(load_input())
    print(part1(passports))
    print(part2(passports))




class PassportValidator:

    OPTIONAL = {'cid'}
    REQUIRED = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

    passport: dict

    def __init__(self, passport: dict):
        self.passport = passport

    def validate(self) -> bool:
        return all(
            getattr(self, field)()
            for field in self.REQUIRED
        )

    def byr(self) -> bool:
        value = self.passport.get('byr')
        return (
            value is not None
            and value.isdigit()
            and 1920 <= int(value) <= 2002
        )

    def iyr(self) -> bool:
        value = self.passport.get('iyr')
        return (
            value is not None
            and len(value) == 4
            and value.isdigit()
            and 2010 <= int(value) <= 2020
        )

    def eyr(self) -> bool:
        value = self.passport.get('eyr')
        return (
            value is not None
            and value.isdigit()
            and 2020 <= int(value) <= 2030
        )

    def hgt(self) -> bool:
        value = self.passport.get('hgt')
        if value is not None:
            match = re.match(r'(\d+)(cm|in)', value)
            size, units = (match is not None and match.groups()) or (0, '')
            lower, upper = (150, 193) if units == 'cm' else (59, 76)
        else:
            lower, upper = 1, 1
            size = '0'
        return lower <= int(size) <= upper

    def hcl(self) -> bool:
        value = self.passport.get('hcl', '')
        match = re.match(r'#[0-9a-f]{6}$', value)
        return match is not None

    def ecl(self) -> bool:
        value = self.passport.get('ecl', '')
        return value in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')

    def pid(self) -> bool:
        value = self.passport.get('pid', '')
        return re.match(r'\d{9}$', value) is not None


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
        if set(PassportValidator.REQUIRED) - set(passport) == set()
    ])


def part2(passports: list) -> int:
    return len([
        passport for passport in passports
        if PassportValidator(passport).validate()
    ])
    return count


if __name__ == '__main__':
    main()
