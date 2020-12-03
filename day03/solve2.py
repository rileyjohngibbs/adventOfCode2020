from functools import reduce


print(len([x for x in [r[(3*i) % len(r)] for i, r in enumerate([r.strip() for r in open('input.txt').readlines()])] if x == '#']))
print(reduce(lambda a, b: a * b, map(lambda m: len([x for x in [r[(m[0]*e//m[1]) % len(r)] for e, r in enumerate([r.strip() for r in open('input.txt').readlines()]) if e % m[1] == 0] if x == '#']), [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]), 1))
