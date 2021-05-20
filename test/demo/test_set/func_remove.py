
s = set()

s.add('a')
s.add('b')
s.add('c')
s.add('d')
s.add('')
print(s)

s.remove('a')
print(s)

s.remove('')
print(s)

if 'd' in s:
    s.remove('d')
print(s)
