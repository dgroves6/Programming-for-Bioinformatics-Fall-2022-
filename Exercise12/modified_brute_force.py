#!/usr/bin/env python3

import argparse
import time
from multiprocessing import Pool, cpu_count

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
parser.add_argument("-t", metavar="<INT: number of threads", required=False, type=int, default=1)
args = parser.parse_args()

out = []
EOF = False
chroms1, chroms2 = [], []

def write_to_file(out):
    h = open(args.out, 'w')
    h = open(args.out, 'a')
    for line in out:
        h.write('\t'.join(line) + '\n')
    h.close()

# Parse input BED file and split into separate chromosomes
def parse_bed_file(file):
    chroms = []
    traversed = []
    with open(file) as f:
        for line in f:
            if (chrom := line.split()[0]) not in traversed:
                traversed.append(chrom)
                chroms.append([])
            chroms[-1].append([chrom] + [int(coord) for coord in line.split()[1:3]])
    return chroms
        
def pointer_algo(input_data):
    te_list, intron_list = input_data[0], input_data[1]
    print(f'Working on {te_list[0][0]}...')
    count = 0
    i, j, break_j = 0, 0, 0
    n = len(te_list) // 10
    z = len(intron_list)
    for x in te_list:
        x1 = x[1]
        x2 = x[2]
        i += 1
        #if i % n == 0:
        #    print(f'{te_list[0][0]} {round(i/len(te_list), 2) * 100}% completed')
        for y in intron_list:
            y1 = y[1]
            y2 = y[2]
            if x2 < y1:
                break
            if y2 < x1:
                continue
            if (min(x2,y2) - max(x1,y1)) * 100 // (x2 - x1) >= args.m:
                count += 1
    return count

def pool_workers(work):
    if args.t > cpu_count():
        args.t = cpu_count()
        print(args.t)
    p = Pool(args.t)
    out = list(p.map(pointer_algo, work))
    p.close()
    p.join()
    return out

def main():
    read_time = time.time()
    te_chroms = parse_bed_file(args.file1)
    print(f"Read time: {time.time()-read_time}")
    intron_chroms = parse_bed_file(args.file2)
    work = tuple(zip(te_chroms, intron_chroms))
    counts = pool_workers(work)
    print(sum(counts))

if __name__ == '__main__':
    main()

end = time.time()
print(end-start)
