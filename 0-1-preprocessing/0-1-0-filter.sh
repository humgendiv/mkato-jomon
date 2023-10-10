#!/bin/bash
#PBS -N filter_vcf
#PBS -o output_file.log
#PBS -e error_file.log
#PBS -l nodes=1:ppn=1
#PBS -l walltime=10:00:00

DIR="/home1/mkato/hdd_data/data/0-0-raw_vcf"
OUTPUT_DIR="/home1/mkato/hdd_data/data/0-1-filtered_vcf"

mkdir -p $OUTPUT_DIR

bcftools filter -e 'INFO/DP<10 || INFO/DP>100' -Oz -o $OUTPUT_DIR/${SAMPLE}_filtered.vcf.gz $DIR/${SAMPLE}.vcf.gz
