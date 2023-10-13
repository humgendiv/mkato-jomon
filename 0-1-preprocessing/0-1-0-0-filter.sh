#!/bin/bash
#PBS -N filter_vcf
#PBS -o output_file.log
#PBS -e error_file.log
#PBS -l nodes=1:ppn=1
#PBS -l walltime=10:00:00

DIR="/home1/mkato/hdd_data/data/0-0-raw_vcf"
OUTPUT_DIR="/home1/mkato/hdd_data/data/0-1-filtered_vcf"

mkdir -p $OUTPUT_DIR
# デプスでフィルター
# クオリティでフィルター
# 染色体のchrの文字列を削除
# 常染色体以外の行を削除
bcftools filter -e 'INFO/DP<10 || INFO/DP>100' $DIR/${SAMPLE}.vcf.gz -Ob | \
bcftools filter -e 'QUAL<30 || QUAL == "."' -Ob | \
bcftools annotate --rename-chrs /home/mkato/mkato-jomon/0-1-preprocessing/rename_chrs.txt -Oz -o $OUTPUT_DIR/${SAMPLE}_filtered2.vcf.gz