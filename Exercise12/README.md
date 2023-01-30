# Programming for Bioinformatics Fall 2022
Bash and Python class assignments for practical applications in bioinformatics

## HW 9: Ortholog Detection with BLAST
Outputs list of reciprocal best hits given two sets of DNA or protein sequences

`./dgroves6_find_orthologs.py -i1 <Input file 1> -i2 <Input file 2> -o <Output file name> –t <Sequence type – n/p>`

Takeaways:
    - Avoid unecessary function calls, especially inside heavy loops
    - Always trace out your algorithm to make sure it's correct (Excel for this case)


Version 4 Modifications:
    - multiprocessing is removed
    - implements pointer/anchor algorithm

Number of Matches: 8185 for chrY, 87890 for chrY+21+22, 2693179 for full TE.bed and Intron.bed
Brute Force - m x n comparisons for each chromosome
                - chrY in 3.1 s     trio in 36.4 s      full in 40 min
Modified Brute Force - turn coords into ints as you read the file
                - chrY in 0.6 s     trio in 10.2 s      full in 9.5 min
Pointer Algorithm - implements a rolling anchor to avoid unecessary comparisons
                - chrY in 0.06 s    trio in 0.7 s       full in 74 s
