#!/bin/bash
#PBS -N split_f23
#PBS -e error_file.log
#PBS -l nodes=1:ppn=1
#PBS -l walltime=10:00:00

#tabix -p vcf /home1/mkato/hdd_data/data/0-1-filtered_vcf/F23_filtered2.vcf.gz
bcftools view -r 1,2,3,4,5,6,7,8 /home1/mkato/hdd_data/data/0-1-filtered_vcf/F23_filtered2.vcf.gz -Oz -o /home1/mkato/hdd_data/data/0-1-filtered_vcf/F23_filtered2_1to8.vcf.gz
#bcftools view -r 9,10,11,12,13,14,15,16,17,18,19,20,21,22 /home1/mkato/hdd_data/data/0-1-filtered_vcf/F23_filtered2.vcf.gz -Oz -o /home1/mkato/hdd_data/data/0-1-filtered_vcf/F23_filtered2_9to22.vcf.gz