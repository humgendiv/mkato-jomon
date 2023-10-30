#!/bin/bash

#$ -cwd
#$ -V
#$ -l short
#$ -l d_rt=01:00:00
#$ -l s_rt=01:00:00
#$ -l s_vmem=8G
#$ -l mem_req=8G
#$ -N bamcaller
#$ -S /bin/bash

DATADIR=/home/mkato/hdd_data/data/
OUTDIR=${DATADIR}/2-msmc

sample_name=$1
depth=$2 # 予め算出してあるaverage depth
chr=$3

bcftools mpileup -q 20 -Q 20 -C 50 -r "chr${3}" -f "${DATADIR}reference/hg19.fa" "$DATADIR/bam/$1.bam" | bcftools call -c -V indels |
/home/mkato/Repo/msmc/msmc-tools/bamCaller.py $depth "${OUTDIR}/${1}_chr${3}_mask.bed.gz" | gzip -c > "${OUTDIR}/${1}_chr${3}.vcf.gz"