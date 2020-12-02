import re


print(len([1 for a, b, c, p in (re.match('(\d+)-(\d+) (.): (.+)', line).groups() for line in open('input.txt').readlines()) if int(a) <= len(re.findall(c, p)) <= int(b)]))
print(len([1 for a, b, c, p in (re.match('(\d+)-(\d+) (.): (.+)', line).groups() for line in open('input.txt').readlines()) if int(p[int(a) - 1] == c) + int(p[int(b) - 1] == c) == 1]))
