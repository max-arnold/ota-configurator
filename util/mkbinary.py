import sys

def dh(x):
  r = ''
  while len(x) > 0:
    r += chr(int(x[0:2], 16))
    x = x[2:]
  return r

f_in = file(sys.argv[1])
f_out = file(sys.argv[2], "wb")

for l in f_in:
  ll = l.strip().split(",")
  for i in ll:
    if i[0:2] == "#$":
      f_out.write(dh(i[2:]))
