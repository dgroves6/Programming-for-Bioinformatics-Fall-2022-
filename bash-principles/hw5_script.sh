#!/bin/bash

#2.1 - DONE
s=0
for i in $(seq 1 100)
do
	s=$(($s+$i))
done
echo $s

#2
foo="Hello"
for ((i=0; i<${#foo}; i++))
do
	echo ${foo:$i:1}
done

# Whenever evaluating booleans or doing arithmetic, put in double parentheses (or use -gt etc with arith and single brackets)
# see Arithmetic Expansion in shell

#3 - DONE
# also could've done until (($x == $y)) or while (($x != $y))
x=0; y=100
until [ $x -eq $y ]
do
	((x++))
	((y--))
done
echo "x and y are equal"


#4 - DONE
<<comment
x=0; y=100
while (($x != $y))
do
	echo $(($x-$y))
    ((x++))
    ((y--))
done
echo "x and y are equal"
comment

#5 - DONE
<<com
while getopts "LGB:" orient
do
	case $orient in
		L) echo "Rock, paper, ... wink, wink";;
		G) echo "Queen, whatchu said?";;
		B) num=$OPTARG; echo "I'm a bicon in $num different countries.";;
	esac
done
com

#6
<<com
echo "Please enter a day:"
read day
case $day in
	Monday) echo "Monday is day number 1";;
	Tuesday) echo "Tuesday is day number 2";;
	Wednesday) echo "Wednesday is day number 3";;
	Thursday) echo "Thursday is day number  4";;
	Friday) echo "Friday is day number 5";;
	Saturday) echo "Saturday is day number 6";;
	Sunday) echo "Sunday is day number 7";;
esac
com

# Mini Challenge 1
# cannot use shell variables within awk quotes -> awk will think they are columns
# ^-- cannot use with single quotes bc bash interprets single quotes literally
# double quotes preserve all literal values except for $, `, and \ --> see Shell Expansion
# ALT ANSWER -> sed -n "/$i/p" rand.txt >> seq$i.fasta -> p dups line $i but instead of printing the dups in addition to the original lines, it just prints the dupes

# Mini Challenge 2
# arithmetic in (())
# reg for loops like (( var=0; var < 9; var++))
# while usually uses [] and -lt -eq -ge etc for comparisons
# $i_$j doesn't work, nor $i\_$j -> use brace expansion to overspecify $x

verbose=false
while getopts "n:m:v" option
do
	case $option in
		n) filenum=$OPTARG; echo "The filenum is $filenum";;
		m) seqnum=$OPTARG; echo "The seqnum is $seqnum";;
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
	
	echo
done

# Mini Challenge 3
# Use getopts in a while loop: each time getopts is called it moves to the next parameter and argument and provides it to you until it exits (exits when there's nothing left to parse)
# $@ refers to all the command line arguments
# can maybe modify to run faster by putting the urandom line outside both loops

