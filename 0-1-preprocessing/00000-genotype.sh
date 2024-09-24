 /home/mkato/Repo/gatk-4.2.0.0/gatk --java-options "-Xmx4g" GenotypeGVCFs \
   --include-non-variant-sites \
   -R /home1/mkato/hdd_data/data/reference/hs37d5_chr.fa \
   -V /home1/mkato/hdd_data/data/fastq/FM027/FM027-1-1.gvcf.gz \
   -O /home/mkato/hdd_data/data/0-0-raw_vcf/FM027-1.vcf.gz
 
