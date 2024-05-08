#!/bin/bash

picard_jar="/home/mkato/Repo/gatk-4.2.0.0/picard.jar"
input_dir="/home/mkato/hdd_data/data/Genomes/korean"
output_dir="/home/mkato/hdd_data/data/Genomes/korean"
chain_file="/home/mkato/hdd_data/data/reference/hg38ToHg19.over.chain.gz"
reference_fasta="/home/mkato/hdd_data/data/reference/hg19.fa"

for i in {1..22}; do
    input_vcf="${input_dir}/chr${i}.recal.vcf"
    output_vcf="${output_dir}/chr${i}.hg19.vcf"
    reject_vcf="${output_dir}/chr${i}_reject.vcf"
    
    nohup java -jar "${picard_jar}" LiftoverVcf \
        I="${input_vcf}" \
        O="${output_vcf}" \
        CHAIN="${chain_file}" \
        REJECT="${reject_vcf}" \
        R="${reference_fasta}" &
done
