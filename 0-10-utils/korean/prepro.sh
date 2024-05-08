#!/bin/bash

input_dir="/home/mkato/hdd_data/data/Genomes/korean/hg19"
output_dir="/home/mkato/hdd_data/data/Genomes/korean/prepro"

for chr in {1..22}; do
  input_file="${input_dir}/chr${chr}.hg19.vcf"
  output_file="${output_dir}/chr${chr}.hg19.prepro.vcf"
  
  awk '{if($0 !~ /^#/) {sub(/^chr/, "", $1); print $1"\t"$2"\t"$1":"$2"\t"$4"\t"$5"\t"$6"\t"$7"\t"$8} else {gsub(/contig=<ID=chr/, "contig=<ID=", $0); print $0}}' "${input_file}" > "${output_file}"
done
