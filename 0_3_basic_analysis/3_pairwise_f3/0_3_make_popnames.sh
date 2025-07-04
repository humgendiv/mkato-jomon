#!/usr/bin/env bash
set -euo pipefail



IND_FILE="/home/mkato/hdd_data/0_3_basic_analysis/3_pairwise_f3/merged_with_1240K.targetpops.ind.fixed"
OUTGROUP="Mbuti"

POPFILE="popnames.txt"

awk '{ split($1,a,":"); print a[1] }' $IND_FILE | sort -u > popnames.txt


mapfile -t pops < "$POPFILE"
{
  for ((i=0; i<${#pops[@]}; i++)); do
    for ((j=i+1; j<${#pops[@]}; j++)); do
      # いずれもアウトグループでない場合のみ
      if [[ "${pops[i]}" != "$OUTGROUP" && "${pops[j]}" != "$OUTGROUP" ]]; then
        printf "%s\t%s\t%s\n" "${pops[i]}" "${pops[j]}" "$OUTGROUP"
      fi
    done
  done
} > poplist.txt
echo "→ poplist.txt generated with $(wc -l < poplist.txt) triples"
