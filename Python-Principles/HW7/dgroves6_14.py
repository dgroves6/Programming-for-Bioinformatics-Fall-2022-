#!/usr/bin/env python3

n = 11
fib = [0,1]
for i in range(n-2):
    fib.append(fib[i] + fib[i+1])
print(fib)