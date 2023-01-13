#!/usr/bin/env python3
import sys

known_file = sys.argv[1]
ref_file = sys.argv[2]
inf_file = sys.argv[3]

# infect genes -> xref IDs -> knownGene coords

# Create list of infectious disease genes
with open(inf_file, 'r') as f:
    infs = sorted(f.read().splitlines()[1:])

# Create refs dict of gene:ID from infectious genes list. 
with open(ref_file, 'r') as f:
    rows = [line.split('\t') for line in f.read().splitlines()]
    refs = {col[4]:col[0] for col in rows[::-1]} # [::-1] gets first occ

# Create known dict of ID:[chrom,start,stop]
with open(known_file, 'r') as f:
    rows = [line.split('\t') for line in f.read().splitlines()]
    known = {col[0]:[col[1], col[3], col[4]] for col in rows}

print('\t'.join(['Gene', 'Chr', 'Start', 'Stop']))
for gene in infs:
    coords = '\t'.join(known[refs[gene]])
    print(gene + '\t' + coords)
