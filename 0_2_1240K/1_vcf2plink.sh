mkdir -p /home/mkato/hdd_data/0_2_1240K

plink2 \
  --vcf /home/mkato/hdd_data/0_1_vcf/merged.1240K.renamed.vcf.gz \
  --max-alleles 2 \
  --make-bed \
  --out /home/mkato/hdd_data/0_2_1240K/jomon_merged
