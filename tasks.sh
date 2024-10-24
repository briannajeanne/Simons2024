#!/bin/bash

set -e

for digit in 0 1 2 3 4 5 6 7 8 9; do
    input="output/${digit}.chr21.10000000_14999999.tsv.gz"
    [ ! -f "$input" ] && continue
    
    for start in 10 11 12 13 14; do
        start_pos="${start}000000"
        end_pos="$((start + 1))000000"
        [ $start -eq 14 ] && end_pos="14999999"
        
        zcat "$input" | \
            awk -F'\t' -v s="$start_pos" -v e="$end_pos" \
                'NR==1 || ($2 >= s && $2 < e)' | \
            gzip > "output/${digit}.chr21.${start_pos}_${end_pos}.tsv.gz"
    done
done
