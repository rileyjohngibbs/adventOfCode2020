print(max(int(r.translate(str.maketrans({'F': '0', 'B': '1', 'L': '0', 'R': '1'})), base=2) for r in open('input.txt').read().split()))
print((lambda t: next(s for s in range(2**10) if s not in t and s + 1 in t and s - 1 in t))({int(r.translate(str.maketrans({'F': '0', 'B': '1', 'L': '0', 'R': '1'})), base=2) for r in open('input.txt').read().split()}))
