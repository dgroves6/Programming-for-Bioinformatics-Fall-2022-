#!/bin/bash

verbose=false
while getopts "n:m:v" option
do
	case $option in
		n) filenum=$OPTARG; echo "The number of requested files is $filenum.";;
		m) seqnum=$OPTARG; echo "The number of sequences per file is $seqnum.";;
		v) verbose=true; echo "Verbose mode was selected!";;
	esac
done

if $verbose; then echo ""; fi

for i in $(seq 1 $filenum)
do
    if [ -a seq$i.fasta ]
    then
		if $verbose; then echo "File seq$i.fasta exists. Removing..."; fi
        rm seq$i.fasta
    fi    
	
	if $verbose; then echo "Creating new file seq$i.fasta..."; fi
	touch seq$i.fasta

	if $verbose; then echo "Generating $j random nucleotide sequences..."; fi
	cat /dev/urandom | tr -dc 'ACGT' | fold -w 50 | head -$seqnum > rand.txt
        
	for j in $(seq 1 $seqnum)
	do
		echo ">seq${i}_${j} for seq$i.fasta" >> seq$i.fasta
		awk "NR == $j {print}" rand.txt >> seq$i.fasta
		if $verbose; then echo "Sequence $j written to seq$i.fasta"; fi
	done
	
	if $verbose; then echo; fi
done

