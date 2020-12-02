import re


def main():
    input_lines = load_input()
    print(part1(input_lines))
    print(part2(input_lines))


def load_input():
    with open('input.txt') as f:
        lines = f.readlines()
    return lines


def part1(input_lines: list):
    return len([
        x for x in input_lines
        if validate_password_1(*parse_line(x))
    ])


def part2(input_lines: list):
    return len([
        x for x in input_lines
        if validate_password_2(*parse_line(x))
    ])


def parse_line(line: str):
    m = re.match(r'(\d+)-(\d+) (.): (.+)', line)
    min_, max_ = int(m.group(1)), int(m.group(2))
    char = m.group(3)
    password = m.group(4)
    return min_, max_, char, password


def validate_password_1(min_: int, max_: int, char: str, password: str):
    return min_ <= len(re.findall(char, password)) <= max_


def validate_password_2(min_: int, max_: int, char: str, password: str):
    return (
        password[min_ - 1] == char and password[max_ - 1] != char
        or password[min_ - 1] != char and password[max_ - 1] == char
    )


if __name__ == '__main__':
    main()
