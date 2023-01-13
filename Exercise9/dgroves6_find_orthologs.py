#!/usr/bin/env python3
import argparse
import subprocess
import os

parser = argparse.ArgumentParser()
parser.add_argument("-i1", metavar="<Input file 1>", help="first file for blast input",
                    required=True, type=str, dest="file1")
parser.add_argument("-i2", metavar="<Input file 2>", help="second file for blast input",
                    required=True, type=str, dest="file2")
parser.add_argument("-o", metavar="<Output file name>", required=False, 
                    default="out.txt", type=str, dest="out")
parser.add_argument("-t", metavar="<Sequence type - n/p>", help="nucelotide or protein sequence", 
                    required=False, default='n', type=str, dest="type")
args = parser.parse_args()

# Determine type of blast to run
if args.type == 'n':
    blast, dbtype = 'blastn', 'nucl'
elif args.type == 'p':
    blast, dbtype = 'blastp', 'prot'

# Make temporary directory
os.mkdir(os.getcwd()+'/temp/')
subprocess.run(['cp', args.file1, args.file2, 'temp/'])
os.chdir(os.getcwd()+'/temp/')

# Make database files (for indexing and faster performance)
subprocess.run(f"makeblastdb -in {args.file1} -dbtype {dbtype}", shell=True)
subprocess.run(["makeblastdb", "-in", args.file2, "-dbtype", dbtype])

# Perform blast search
subprocess.run(f"{blast} -query {args.file1} -db {args.file2} -out best1.txt -outfmt 6 -max_target_seqs 1 -max_hsps 1", shell=True)
subprocess.run([blast, "-query", args.file2, "-db", args.file1, "-out", "best2.txt", "-outfmt", "6", 
                "-max_target_seqs", "1", "-max_hsps", "1"])

# Create dicts of best hits for each blast run
dict1, dict2 = {}, {}

with open('best1.txt') as f:
    for line in f:
        pair = line.split()[0:2]
        dict1[pair[0]] = pair[1]

with open('best2.txt') as f:
    for line in f:
        pair = line.split()[0:2]
        dict2[pair[0]] = pair[1]

# Get reciprocal best hits and write them to the output file
with open(args.out, 'w') as f:
    for k,v in dict1.items():
        if v in dict2.keys() and dict2[v] == k:
            f.write(k + ' ' + v + '\n')

# Remove the temporary directory
subprocess.run(['mv', args.out, '../'])
os.chdir('../')
subprocess.run(['rm', '-rf', 'temp/'])

"""
# Compare output and test files
outdict, sampdict = {}, {}
with open(args.o) as f:
    for line in f:
        pair = line.split()
        outdict[pair[0]] = pair[1]

with open('sample_output.txt') as f:
    for line in f:
        pair = line.split()
        sampdict[pair[1]] = pair[0]

with open('outdict.txt', 'w') as f:
    for k in sorted(outdict.keys()):
        f.write(k + ' ' + outdict[k] + '\n')

with open('sampdict.txt', 'w') as f:
    for k in sorted(sampdict.keys()):
        f.write(k + ' ' + sampdict[k] + '\n')
"""

### NOTES
# Can either run subprocess with string and shell=True or list and shell=False
# Each query can have multiple target seqs ranked from best E-value to worst
# Each target seq can have multiple High-scoring Segment Pairs (ie, multiple high-scoring local alignments)
# Setting -max_target_seqs=1 shows the highest-scoring target seq
# Setting -max_hsps=1 only shows the HSP (local alignment) with the highest score
# Setting -outfmt 6 make a concise tabular view without extra verbose information
# tempfile module can make temporary directories