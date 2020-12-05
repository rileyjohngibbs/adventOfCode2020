def main():
    input_ = load_input()
    print(part1(input_))
    print(part2(input_))


def load_input():
    with open('input.txt') as f:
        return [r.strip() for r in f.readlines()]


def part1(input_: list) -> int:
    return max(8 * r + c for r, c in map(get_row_and_column, input_))


def part2(input_: list) -> int:
    ticketed_ids = {8 * r + c for r, c in map(get_row_and_column, input_)}
    row, col = next(
        id_to_row_and_column(seat_id)
        for seat_id in range(128 * 8)
        if seat_id not in ticketed_ids
        and seat_id + 1 in ticketed_ids
        and seat_id - 1 in ticketed_ids
    )
    return 8 * row + col


def get_row_and_column(directions: str) -> tuple:
    rows = list(range(128))
    for row_dir in directions[:7]:
        if row_dir == 'F':
            rows = rows[:len(rows)//2]
        else:
            rows = rows[len(rows)//2:]
    cols = list(range(8))
    for col_dir in directions[7:]:
        if col_dir == 'L':
            cols = cols[:len(cols)//2]
        else:
            cols = cols[len(cols)//2:]
    return rows[0], cols[0]


def id_to_row_and_column(seat_id: int) -> tuple:
    column = seat_id % 8
    row = seat_id // 8
    return row, column


if __name__ == '__main__':
    main()
