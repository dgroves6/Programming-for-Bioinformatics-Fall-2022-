# Exercise 12 - Overlap Algorithm
Details of test cases, previous versions, and general notes for the problem

## Test Cases
- small test - chrY
- big test - chrY, chr21, & chr22

## Previous Versions
`incorrect_with_fxns.py` and `incorrect_wo_fxns.py`
- original attempts with incorrect algorithms

`brute_force.py`
- brute force method to determine the correct number of overlaps by m x n comparisons
- uses multiprocessing to speed it up

`modified_brute_force.py`
- changed coord datatype from str to int as the file was read
- as opposed to originally doing m x n type conversions

`../dgroves6_overlapBed.py`
- implements a rolling anchor/pointer algorithm to avoid unecessary comparisons
- removed multiprocessing module

## Takeaways:
- Avoid unecessary function calls, especially inside heavy loops
- Always trace out your algorithm to make sure it's correct (Excel for this case)

## Time Comparisons
- Correct Numbers of Matches: 
    - 8185 for chrY
    - 87890 for trio
    - 2693179 for full TE.bed and Intron.bed
- Brute Force
    - chrY in 3.1 s
    - trio in 36.4 s
    - full in 40 min
- Modified Brute Force
    - chrY in 0.6 s
    - trio in 10.2 s
    - full in 9.5 min
- Pointer Algorithm
    - chrY in 0.06 s
    - trio in 0.7 s
    - full in 74 s
