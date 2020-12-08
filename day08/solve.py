import re


def main():
    input_ = load_input()
    print(part1(input_))
    print(part2(input_))


def load_input():
    with open('input.txt') as f:
        return [r.strip() for r in f.readlines()]


def part1(input_: list):
    instructions = [
        [*re.match(r'(.{3}) (.*)', row).groups(), 0]
        for row in input_
    ]
    _, acc = run_to_loop(instructions)
    return acc


def run_to_loop(instructions):
    instructions = [i[:] for i in instructions]
    acc, index = 0, 0
    while index < len(instructions) and instructions[index][-1] == 0:
        op = instructions[index][0]
        instructions[index][-1] += 1
        if op == 'nop':
            index += 1
        elif op == 'acc':
            acc += int(instructions[index][1])
            index += 1
        else:
            index += int(instructions[index][1])
    looped = index < len(instructions)
    return looped, acc


def part2(input_: list):
    instructions = [
        [*re.match(r'(.{3}) (.*)', row).groups(), 0]
        for row in input_
    ]
    for i, instr in enumerate(instructions):
        op_change = {'nop': 'jmp', 'jmp': 'nop'}.get(instr[0])
        if op_change is None:
            continue
        modded_instrs = [*instructions[:i], [op_change, *instr[1:]], *instructions[i+1:]]
        looped, acc = run_to_loop(modded_instrs)
        if not looped:
            break
    else:
        raise Exception()
    return acc


if __name__ == '__main__':
    main()
