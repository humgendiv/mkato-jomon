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

DATADIR=/home/mkato/hdd_data/data/2-msmc
OUTDIR=$DATADIR/${sample}_${sample_ref}/msmc_input_file
MSMC_TOOLS=/home/mkato/Repo/msmc/msmc-tools
mkdir -p $OUTDIR
ref_mask=/home/mkato/hdd_data/data/reference/ref_masks/hs37d5_chr${chr}.mask.bed


/home/mkato/Repo/msmc/msmc-tools/generate_multihetsep.py \
--mask="${DATADIR}/${sample_ref}/${sample_ref}_${chr}_mask.bed.gz" \
--mask="${DATADIR}/${sample}/${sample}_${chr}_mask.bed.gz" \
--mask=$ref_mask \
"${DATADIR}/${sample_ref}/${sample_ref}_${chr}.vcf.gz" \
"${DATADIR}/${sample}/${sample}_${chr}.vcf.gz" \
> $OUTDIR/${sample}_joined_to_${sample_ref}.${chr}.multihetsep.txt


#/home/mkato/Repo/msmc/msmc-tools/generate_multihetsep.py \
#--chr $chr \
#--mask="${DATADIR}/${sample}/${sample}_chr${chr}_mask.bed.gz" \
#--mask=$ref_mask \
#"${DATADIR}/${sample}/${sample}_chr${chr}.vcf.gz" > $OUTDIR/${sample}.chr${chr}.multihetsep.txt
