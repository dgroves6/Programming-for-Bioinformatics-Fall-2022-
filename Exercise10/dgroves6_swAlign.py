#!/usr/bin/env python3
import sys

file1 = sys.argv[1]
file2 = sys.argv[2]

MATCH = 1
MISMATCH = -1
GAP = -1

# Read in files to get sequences and lengths
with open(file1) as f:
    seq1 = f.readlines()[1].strip()
    m = len(seq1)

with open(file2) as f:
    seq2 = f.readlines()[1].strip()
    n = len(seq2)

# Create the NW matrix with gap penalties -> matrix
def initialize_matrix(m:int, n:int):

    # Create empty matrix
    mat = []
    for i in range(m+1):
        mat.append([])
        for j in range(n+1):
            mat[i].append([])

    # Fill in gap penalties
    mat[0][0] = 0

    for i in range(1,m+1):
        mat[i][0] = 0

    for j in range(1,n+1):
        mat[0][j] = 0

    return mat

# Score the matrix -> matrix
def do_scoring(mat:list):
    for i in range(1,m+1):
        for j in range(1,n+1):
            if seq1[i-1] == seq2[j-1]:
                s = MATCH
            else:
                s = MISMATCH   

            up = mat[i-1][j] + GAP
            left = mat[i][j-1] + GAP
            diag = mat[i-1][j-1] + s

            mat[i][j] = max(up, left, diag, 0)
    return mat

# Choose the direction to move during traceback -> (new_i, new_j, dir)
def choose_traceback_dir(mat:list, i:int, j:int):
    # Edge case: touching the top edge
    try:
        t = mat[i-1]
    except IndexError as e:
        return (i,j-1,'left')

    # Edge case: touching the left edge
    try:
        t = mat[i][j-1]
    except IndexError as e:
        return (i-1,j,'up')

    # Touching no edge: [diag, up, left]
    cmax = max([mat[i-1][j-1], mat[i-1][j], mat[i][j-1]])
    if cmax == mat[i-1][j-1]:
        return (i-1,j-1,'diag')
    elif cmax == mat[i-1][j]:
        return (i-1,j,'up')
    else:
        return (i,j-1,'left')

# Perform traceback
def do_traceback(mat:list):
    # Find highest-scoring value to start traceback
    amax = 0
    for a in range(m+1):
        for b in range(n+1):
            if mat[a][b] > amax:
                i, j, amax = a, b, mat[a][b]
    alignment = []

    while mat[i][j] != 0:
        if seq1[i-1] == seq2[j-1]:
            alignment.append((seq1[i-1], seq2[j-1]))
            i-=1
            j-=1
        else:
            x, y, dir = choose_traceback_dir(mat, i, j)
            if dir == 'diag':
                alignment.append((seq1[i-1], seq2[j-1]))
            elif dir == 'up':
                alignment.append((seq1[i-1], '-'))
            else:
                alignment.append(('-', seq2[j-1]))
            i, j = x, y
    return alignment
            
# Print alignment and score to STDOUT
def print_output(alignment:list):
    s1 = ''.join([x[0] for x in alignment[::-1]])
    s2 = ''.join([x[1] for x in alignment[::-1]])
    c = []
    score = 0
    for x in alignment[::-1]:
        if x[0] == x[1]:
            c.append('|')
            score+=MATCH
        elif x[0] == '-' or x[1] == '-':
            c.append(' ')
            score+=GAP
        else:
            c.append('*')
            score+=MISMATCH
    print(s1)
    print(''.join(c))
    print(s2)
    print('Alignment score:', score)

def main():
    init = initialize_matrix(m, n)
    scored = do_scoring(init)
    align = do_traceback(scored)
    print_output(align)

if __name__ == '__main__':
    main()




### NOTES

# Traceback
# Starts from highest-scoring value
# If MATCH -> diag
# If MISMATCH -> max(left, diag, up)
    # If up, gap is introduced in the sequence that's up
    # If left, gap is introduced in the sequence to the left
# Ties are broken in this preference: diag, up, left