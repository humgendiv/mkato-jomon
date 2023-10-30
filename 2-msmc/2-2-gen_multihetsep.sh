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

DATADIR=/home/mkato/hdd_data/data/2-msmc/
#chr=$1

OUTDIR="${DATADIR}/msmc_input_file"

ref_mask="/home/mkato/hdd_data/data/reference/ref_masks/hs37d5_chr${chr}.mask.bed"

/home/mkato/Repo/msmc/msmc-tools/generate_multihetsep.py \
--mask="${DATADIR}I4_chr${chr}_mask.bed.gz" \
--mask="${DATADIR}T5_chr${chr}_mask.bed.gz" \
--mask=$ref_mask \
"${DATADIR}/I4_chr${chr}.vcf.gz" "${DATADIR}/T5_chr${chr}.vcf.gz" > $OUTDIR/T5I4.chr${chr}.multihetsep.txt