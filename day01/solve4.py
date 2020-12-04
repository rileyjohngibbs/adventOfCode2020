print((lambda input_: next(x * y for x in input_ for y in input_ if x + y == 2020))([int(r) for r in open('input.txt').readlines()]))
print((lambda input_: next(x * y * z for x in input_ for y in input_ for z in input_ if x != y and y != z and x != z and x + y + z == 2020))([int(r) for r in open('input.txt').readlines()]))
