#!/bin/bash

for file in output/*.tsv.gz; do
    printf "%s " "$file"
    zcat "$file" | awk '
        {words += NF} 
        END {print words}
    '
done | sort
