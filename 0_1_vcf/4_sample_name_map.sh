bcftools reheader -s /home/mkato/hdd_data/0_1_vcf/sample_name_map.tsv -o /home/mkato/hdd_data/0_1_vcf/merged.1240K.renamed.vcf.gz /home/mkato/hdd_data/0_1_vcf/merged.1240K.vcf.gz
bcftools index -t /home/mkato/hdd_data/0_1_vcf/merged.1240K.renamed.vcf.gz
