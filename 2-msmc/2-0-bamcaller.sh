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
OUTDIR=${DATADIR}/2-msmc/$sample_name/


if [ "$sample_name" = "T5" ]; then
/usr/bin/bcftools mpileup -q 5 -Q 5 -C 50 -Ou -r "chr${chr}" -f "${DATADIR}reference/hg19.fa" "$DATADIR/bam/share/T5_p1_p2_p3.bam" | bcftools call -c -V indels |
/home/mkato/Repo/msmc/msmc-tools/bamCaller.py $depth "${OUTDIR}/${sample_name}_chr${chr}_mask.bed.gz" | gzip -c > "${OUTDIR}/${sample_name}_chr${chr}.vcf.gz"
elif [ "$sample_name" = "I4" ]; then
/usr/bin/bcftools mpileup -q 5 -Q 5 -C 50 -Ou -r "chr${chr}" -f "${DATADIR}reference/hg19.fa" "$DATADIR/bam/share/I4_filtered_RG_dedup_trim.bam" | bcftools call -c -V indels |
/home/mkato/Repo/msmc/msmc-tools/bamCaller.py $depth "${OUTDIR}/${sample_name}_chr${chr}_mask.bed.gz" | gzip -c > "${OUTDIR}/${sample_name}_chr${chr}.vcf.gz"
elif [ "$sample_name" = "NA18939" ]; then
/usr/bin/bcftools mpileup -q 20 -Q 20 -C 50 -Ou -r "chr${chr}" -f "${DATADIR}reference/hg19.fa" "$DATADIR/bam/share/NA18939_updated.bam" | bcftools call -c -V indels |
/home/mkato/Repo/msmc/msmc-tools/bamCaller.py $depth "${OUTDIR}/${sample_name}_chr${chr}_mask.bed.gz" | gzip -c > "${OUTDIR}/${sample_name}_chr${chr}.vcf.gz"
fi