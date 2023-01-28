#!/usr/bin/env python3

import argparse
import time

start = time.time()

# Parse input BED file and separate chromosomes
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
        
# Get list of coords that meet the minimum overlap
def pointer_algo2(input_data):
    te_list, intron_list = input_data[0], input_data[1]
    count, anchor, j = 0, 0, 0
    out = []
    for x in te_list:
        first_overlap = False
        j = anchor
        for y in intron_list[anchor:]:
            if y[1] > x[2]: # y onward is outside the range of x
                break
            if y[2] < x[1]: # no overlap
                j += 1
                continue
            if first_overlap == False:
                first_overlap = True
                anchor = j
            if (min(x[2],y[2]) - max(x[1],y[1])) * 100 // (x[2] - x[1]) >= args.m:
                count += 1
                if args.j:
                    out.append(x + y)
                else:
                    out.append(x)

    print(f'-------------------------{te_list[0][0]} complete')
    return out

# Map the func to each chromosome, and write to the output file
def write_to_file(outputs):
    h = open(args.o, 'w')
    h = open(args.o, 'a')
    for chrom in outputs:
        for coord in chrom:
            line = '\t'.join([str(c) for c in coord])
            h.write(line + '\n')
    h.close()

def main():
    RT = time.time()
    te_chroms = parse_bed_file(args.file1)
    intron_chroms = parse_bed_file(args.file2)
    print(f"Read time: {time.time()-RT}")
    work = tuple(zip(te_chroms, intron_chroms))
    outputs = list(map(pointer_algo2, work))
    total = sum([len(x) for x in outputs])
    print(f'Total overlap: {total}')
    WT = time.time()
    write_to_file(outputs)
    print(f"Write time: {time.time()-WT}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i1", metavar="<input file 1>", help="Coorinate file in BED format",
                        required=True, type=str, dest="file1")
    parser.add_argument("-i2", metavar="<input file 2>", help="Coorinate file in BED format",
                        required=True, type=str, dest="file2")
    parser.add_argument("-m", metavar="<INT: minimal overlap>", help="Minimum percent overlap",
                        required=True, type=int)
    parser.add_argument("-j", help="Join the two entries side by side", action='store_true')
    parser.add_argument("-o", metavar="<output file>", help="file for element count",
                        required=True, type=str)
    args = parser.parse_args()
    main()

end = time.time()
print('Total run time:', end-start)