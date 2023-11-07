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

DATADIR=/home1/mkato/hdd_data/data/2-msmc/
OUTDIR="${DATADIR}/msmc_input_file"

ref_mask="/home1/mkato/hdd_data/data/reference/ref_masks/hs37d5_chr${chr}.mask.bed"

#/home/mkato/Repo/msmc/msmc-tools/generate_multihetsep.py \
#--mask="${DATADIR}/I4/I4_chr${chr}_mask.bed.gz" \
#--mask="${DATADIR}/T5/T5_chr${chr}_mask.bed.gz" \
#--mask=$ref_mask \
#"${DATADIR}/I4/I4_chr${chr}.vcf.gz" "${DATADIR}/T5/T5_chr${chr}.vcf.gz" > $OUTDIR/T5I4.chr${chr}.multihetsep.txt


/home/mkato/Repo/msmc/msmc-tools/generate_multihetsep.py \
--chr $chr \
--mask="${DATADIR}/${sample}/${sample}_chr${chr}_mask.bed.gz" \
--mask=$ref_mask \
"${DATADIR}/${sample}/${sample}_chr${chr}.vcf.gz" > $OUTDIR/${sample}.chr${chr}.multihetsep.txt