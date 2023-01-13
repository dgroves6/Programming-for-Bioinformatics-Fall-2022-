#!/usr/bin/env python3

import argparse
from multiprocessing import Pool
import subprocess

parser = argparse.ArgumentParser(
    prog='parallel_ani',
    description="Perform an all-again-all pairs computation of ANI for given fasta files.",
    epilog="Run the following command to delete temporary files:\nrm *coords *delta *diff *report *snps"
    )
    
parser.add_argument("-o", metavar="<Output file>", 
                    required=True, type=str)
parser.add_argument("-t", metavar="<Number of threads>", 
                    required=False, type=int, default=1)
parser.add_argument('files', nargs='*', help="The list of FASTA files to compare")
args = parser.parse_args()

work = [(x,y) for x in args.files for y in args.files if x != y]

def dnadiff(pair:list):
    pref = pair[0][:-6] + '-' + pair[1][:-6]
    subprocess.run(['dnadiff', '-p', pref] + list(pair), capture_output=True)
    with open(f'{pref}.report') as f:
        for _ in range(18):
            next(f)
        ani = f.readline().split()[1]
    return pair, ani

def pool_handler():
    p = Pool(args.t)
    scores = list(p.map(dnadiff, work))
    p.close()
    p.join()
    return scores

def initialize_matrix(scores:list):
    n = len(args.files) + 1
    mat = [['' for _ in range(n)] for _ in range(n)]
    for i, x in enumerate(args.files):
        mat[0][i+1] = x
        mat[i+1][0] = x
    for i, x in enumerate(args.files):
        for j, y in enumerate(args.files):
            if i == j:
                mat[i+1][j+1] = '100.0000'
            for item in scores:
                if item[0][0] == x and item[0][1] == y:
                    mat[i+1][j+1] = item[1]
    return mat

scores = pool_handler()
mat = initialize_matrix(scores)
h = open(args.o, 'w')
for row in mat:
    h.write('\t'.join(row) + '\n')
h.close()