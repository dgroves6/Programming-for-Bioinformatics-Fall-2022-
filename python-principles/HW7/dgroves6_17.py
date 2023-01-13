#!/usr/bin/env python3

a = [4,35,67,8,9,0,1,1,1,4,3,5,27]
b = [99,100,53,48,72,93,100]

print([sorted(a)[int(len(a)/2)], sorted(b)[int(len(b)/2)]])

# out = [sorted(a)[math.ceil(len(a)/2)+1], sorted(b)[math.ceil(len(b)/2)]]
# can't used a.sort()[] bc sort() returns none
# print(math.ceil(len(a)/2))