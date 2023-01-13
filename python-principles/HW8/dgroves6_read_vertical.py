#!/usr/bin/env python3

import sys

k = int(sys.argv[1])
file = sys.argv[2]

f = open(file, 'r')
line = f.readline().strip().split()
num = len(line)

# can't use with open() and try/except bc for k=0, you get col[-1] => no error
if k == 0 or k > num:
    print('"k" value exceeds the file size')
    f.close()
else:
    first = [line[k-1]]
    rest = [cols.split()[k-1] for cols in f.read().splitlines()]
    # read() continues where readline() left off, so have to append them
    first.extend(rest)
    print('\n'.join(first))
    f.close()