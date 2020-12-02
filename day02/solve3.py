print(len([1 for a, b, c, p in map(lambda s: s.replace('-', ',').replace(':', '').replace(' ', ',').split(','), open('input.txt').readlines()) if int(a) <= p.count(c) <= int(b)]))
print(len([1 for a, b, c, p in map(lambda s: s.replace('-', ',').replace(':', '').replace(' ', ',').split(','), open('input.txt').readlines()) if int(p[int(a) - 1] == c) + int(p[int(b) - 1] == c) == 1]))
