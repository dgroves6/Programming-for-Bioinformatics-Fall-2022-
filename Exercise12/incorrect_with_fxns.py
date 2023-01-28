#!/usr/bin/env python3

import argparse
import time

start = time.time()

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

def count_overlaps(): 

    chroms1, chroms2 = [], []
    i, j, = 0, 0

    with open(args.file1) as f:
        raw1 = f.readlines()
        n = len(raw1)-1

    with open(args.file2) as g:
        raw2 = g.readlines()
        m = len(raw2)-1

    h = open(args.out, 'w')
    h = open(args.out, 'a')

    while True:

        # Check if last line of both or either files is reached
        if i == n and j == m:
            #print(raw1[-1].split()[0])
            return
        elif i == n:
            i -= 1
            j += 1
        elif j == m:
            j -= 1
            i += 1
        else:
            pass

        # Extract coordinates from a single line
        x = raw1[i].split()
        y = raw2[j].split()
        x1, x2 = int(x[1]), int(x[2])
        y1, y2 = int(y[1]), int(y[2])

        # Check that the two line's chromosomes are the same
        # If the chromosomes are different, skip ahead until they're the same
        if x[0] == y[0]:
            pass
        elif x[0] not in chroms1 and y[0] not in chroms2:
            chroms1.append(x[0])
            chroms2.append(y[0])
            #print(x[0])
        elif y[0] not in chroms1:
            i += 1
            continue
        else:
            j += 1
            continue

        # If there is no overlap between coordinates, skip to the next line
        if x2 < y1: # If x before y
            i += 1
            continue

        if x1 > y2: # If y before x
            j += 1
            continue

        if y1 == y2: # If y start and stop are the same
            j += 1
            continue

        # If there is overlap, calculate percent overlap
        if (min(x2,y2) - max(x1,y1)) * 100 // (y2 - y1) >= args.m:
            if args.j: # Join files if -j flag given
                h.write('\t'.join(x+y) + '\n')
            else:
                h.write('\t'.join(x) + '\n')

        # Choose to increment the line of either file
        if y1 < x1:
            j += 1
            continue
        elif x1 < y1:
            i += 1
            continue
        elif x2 < y2:
            i += 1
            continue
        elif y2 < x2:
            j += 1
            continue
        else:
            pass

        h.close()

def main():
    count_overlaps()


if __name__ == '__main__':
    main()

end = time.time()
print(end-start)