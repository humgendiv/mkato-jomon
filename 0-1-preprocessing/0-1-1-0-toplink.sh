#!/bin/bash
#PBS -N vcf_to_plink
#PBS -e error_file.log
#PBS -l nodes=1:ppn=1
#PBS -l walltime=10:00:00

DIR=/home1/mkato/hdd_data/data/
INPUT_DIR=${DIR}/0-1-filtered_vcf
OUTPUT_DIR=${DIR}/0-2-plink

/usr/local/bin/plink --make-bed --allow-extra-chr --vcf ${INPUT_DIR}/${SAMPLE}_filtered2_1to8.vcf.gz --out ${OUTPUT_DIR}/${SAMPLE}_1to8 --memory 90000
#/usr/local/bin/plink --make-bed --allow-extra-chr --vcf ${INPUT_DIR}/${SAMPLE}_filtered2_9to22.vcf.gz --out ${OUTPUT_DIR}/${SAMPLE}_9to22 --memory 90000
