from timeit import timeit


def print_time(module: str, function: str):
    execution = f'{function}(input_)'
    setup = f'from {module} import load_input, {function}; input_ = load_input()'
    runtime = timeit(execution, setup, number=1000)
    print(f'Runtime for {module}.{function}: {runtime}')


for module, function in (
    ('solve', 'part1'), ('solve', 'part2'),
    ('solve2', 'part1'), ('solve2', 'part2'),
    ('solve3', 'part1'),  #('solve3', 'part2'),
):
    print_time(module, function)
