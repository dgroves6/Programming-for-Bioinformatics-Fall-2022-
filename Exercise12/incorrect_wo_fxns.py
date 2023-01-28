#!/usr/bin/env python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i1", metavar="<input file 1>", help="Coorinate file in BED format",
                    required=True, type=str, dest="file1")
parser.add_argument("-i2", metavar="<input file 2>", help="Coorinate file in BED format",
                    required=True, type=str, dest="file2")
parser.add_argument("-m", metavar="<INT: minimal overlap>", help="Minimum percent overlap",
                    required=True, type=int)
parser.add_argument("-j", help="Join the two entries side by side", action='store_true')
parser.add_argument("-o", metavar="<output file>", help="file for element count",
                    required=True, type=str, dest="out")
args = parser.parse_args()

out = []
EOF = False
chroms1, chroms2 = [], []

# Get raw coordinate data and number of lines in file
def read_file(file:str):
    with open(file) as f:
        raw = f.readlines()
        n = len(raw) - 1
    return raw, n

# Go to the next line of one of the files
def increment(x, y, i, j):
    x1, x2 = int(x[1]), int(x[2])
    y1, y2 = int(y[1]), int(y[2])

    if y1 < x1:
        return i, j+1
    elif x1 < y1:
        return i+1, j
    elif x2 < y2:
        return i+1, j
    elif y2 < x2:
        return i, j+1
    else:
        return i, j

# Special increment() function if EOF is reached
def handle_EOF(i:int, n:int, j:int, m:int):
    global EOF
    if i == n and j == m:
        EOF = True
        return None, None
    elif i == n:
        return i-1, j+1
    elif j == m:
        return i+1, j-1
    else:
        return i, j

# Special increment() function if chromosomes are different
def inc_chromosome(x0, y0, i, j):
    global chroms1
    global chroms2
    if x0 not in chroms1 and y0 not in chroms2:
        chroms1.append(x0)
        chroms2.append(y0)
        #print(x0)
        return i, j
    elif y0 not in chroms1:
        return i+1, j
    else:
        return i, j+1

# Check if there is any overlap between the coordinates
def check_overlap(x:list, y:list, i:int, j:int):
    
    x1, x2 = int(x[1]), int(x[2])
    y1, y2 = int(y[1]), int(y[2])

    overlap = False
    
    if x2 < y1:
        return overlap, i+1, j
    elif x1 > y2:
        return overlap, i, j+1
    elif y1 == y2:
        return overlap, i, j+1
    else:
        overlap = True
        return overlap, i, j

# Calculate overlap and append coords if they are above threshold
def calculate_overlap(x:list, y:list):
    global out
    x1, x2 = int(x[1]), int(x[2])
    y1, y2 = int(y[1]), int(y[2])

    if (min(x2,y2) - max(x1,y1)) * 100 // (x2 - x1) >= args.m:
        if args.j:
            out.append(x+y)
        else:
            out.append(x)


def write_to_file(out):
    h = open(args.out, 'w')
    h = open(args.out, 'a')
    for line in out:
        h.write('\t'.join(line) + '\n')
    h.close()

def count_overlaps(): 

    i, j, = 0, 0
    raw1, n = read_file(args.file1)
    raw2, m = read_file(args.file2)

    while EOF == False:

        # Check if EOF is reached
        if i == n or j == m:
            i, j = handle_EOF(i, n, j, m)
        if EOF == True:
            continue

        # Extract coordinates
        x = raw1[i].split()
        y = raw2[j].split()

        # Make sure the chromosomes are the same
        if x[0] != y[0]:
            i, j = inc_chromosome(x[0], y[0], i, j)
            continue

        # If there is no overlap between coordinates, skip to the next iteration
        overlap, i, j = check_overlap(x, y, i, j)

        if overlap == True:
            calculate_overlap(x,y)
        else:
            continue

        i, j = increment(x, y, i, j)


def main():
    count_overlaps()
    write_to_file(out)

if __name__ == '__main__':
    main()
