print(sum(len(set.union(*map(set, g))) for g in [g.split() for g in open('input.txt').read().split('\n\n')]))
print(sum(len(set.intersection(*map(set, g))) for g in [g.split() for g in open('input.txt').read().split('\n\n')]))
