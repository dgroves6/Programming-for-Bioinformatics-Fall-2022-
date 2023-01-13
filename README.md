# Programming for Bioinformatics Fall 2022
Bash and Python class assignments for practical applications in bioinformatics

## HW 9: Ortholog Detection with BLAST
Outputs list of reciprocal best hits given two sets of DNA or protein sequences

`./dgroves6_find_orthologs.py -i1 <Input file 1> -i2 <Input file 2> -o <Output file name> –t <Sequence type – n/p>`


## HW 10: Implementation of Alignment Algorithms
Perform global and local alignments on two DNA sequences. Prints the resulting alignment.

Needleman-Wunsch for global alignment:

`./dgroves6_nwAlign.py seq1_nw.fa seq2_nw.fa`

Smith-Waterman for local alignment:

`./dgroves6_swAlign.py seq1_sw.fa seq2_sw.fa`


## HW 13: Parallelization of Average Nucleotide Identity Calculations
Performs multithreaded all-against-all ANI calculations on given FASTA files

`./parallel_ani.py -o <Output file> [-t <Number of threads>] fasta_file1 fasta_file2 fasta_file3 ...`

