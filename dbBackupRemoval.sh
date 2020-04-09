#!/bin/bash


for i in 1 2 3
	do
	dir="/home/ubuntu/backups/databaser/db$i"
	ant=$(ls $dir | wc -l)

	while [[ $ant -ge 8 ]]
	do
		output=$(ls $dir -tA | tail -1)
		rm "$dir/$output"
		ant=$((ant - 1))
	done
done
