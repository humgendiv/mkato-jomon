#!/usr/bin/env bash
DATADIR=/home/mkato/hdd_data/data/2-msmc/
SAMPLE1="FM020_sorted"
SAMPLE2="F23"
OUTDIR=$DATADIR/FM020_sorted-F23/

MAPDIR=/home/mkato/hdd_data/data/reference/ref_masks/

for chr in {1..22}
do
/home/mkato/Repo/msmc/msmc-tools/generate_multihetsep.py --chr $chr \
    --mask $DATADIR/${SAMPLE1}/modified_mask_and_vcf/${SAMPLE1}_${chr}_mask.bed.gz --mask $DATADIR/${SAMPLE2}/modified_mask_and_vcf/${SAMPLE2}_${chr}_mask.bed.gz \
    --mask $MAPDIR/hs37d5_chr${chr}.mask.bed \
    $DATADIR/${SAMPLE1}/modified_mask_and_vcf/${SAMPLE1}_${chr}.vcf.gz $DATADIR/${SAMPLE2}/modified_mask_and_vcf/${SAMPLE2}_${chr}.vcf.gz \
    > $OUTDIR/FM020_sorted-F23.chr${chr}.multihetsep.txt
done