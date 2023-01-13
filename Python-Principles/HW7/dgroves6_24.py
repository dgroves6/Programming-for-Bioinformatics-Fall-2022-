#!/usr/bin/env python3

seq = 'ACACTGT'

table = str.maketrans('ACGT','TGCA')
rev_comp = seq[::-1].translate(table)
mid = int(len(seq)/2)

if seq[:mid] == rev_comp[:mid]:
    print("Yes")
else:
    print("No")