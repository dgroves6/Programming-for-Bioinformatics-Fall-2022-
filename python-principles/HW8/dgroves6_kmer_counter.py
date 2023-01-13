#!/usr/bin/env python3

import sys

k = int(sys.argv[1])
file = sys.argv[2]

with open(file, 'r') as f:
    raw = f.read().splitlines()
    fasta = "".join(raw[1:])

kdict = {}
for i in range(len(fasta)-k+1):
    kmer = fasta[i:i+k]
    if kmer in kdict.keys():
        kdict[kmer] += 1
    else:
        kdict[kmer] = 1

for key in sorted(kdict.keys()):
    print(key+"\t"+str(kdict[key]))

'''
print(len(fasta))
mycount = set(fasta)
mydict = {}
for elem in mycount:
    countchar = fasta.count(elem)
    mydict[elem] = countchar
print(mydict)
'''