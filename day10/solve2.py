print((lambda c: c[0] * c[1])((lambda f: lambda *a: f(f, *a))(lambda r, f, i, b: b if not i else r(r, f, i[1:], f(b, i[0])))(lambda c, x: (c[0] + (x == 1), c[1] + (x == 3)), (lambda oa: [b - a for a, b in zip([0, *oa], [*oa, oa[-1] + 3])])(sorted(int(r.strip()) for r in open('input.txt').readlines())), (0, 0))))
print((lambda f: lambda *a: f(f, *a))(lambda r, f, i, b: b if not i else r(r, f, i[1:], f(b, i[0])))(lambda a, b: a * ((lambda f: lambda *a: f(f, *a))(lambda f, n: [1, 1, 1, 2, 4, 7][n] if n < 6 else 2*f(f, n-1) - f(f, n-2) + 2**(n-5) + 1)(b)), ((lambda f: lambda *a: f(f, *a))(lambda r, f, i, b: b if not i else r(r, f, i[1:], f(b, i[0])))(lambda c, x: (c[0] + (c[1],) * (x == 3), c[1] * (x == 1) + 1), (lambda oa: [b - a for a, b in zip([0, *oa], [*oa, oa[-1] + 3])])(sorted(int(r.strip()) for r in open('input.txt').readlines())), (tuple(), 1))[0]), 1))
