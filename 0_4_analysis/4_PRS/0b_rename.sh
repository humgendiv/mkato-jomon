bcftools reheader -s /home/mkato/hdd_data/0_1_vcf/sample_name_map.tsv -o /home/mkato/hdd_data/0_4_analysis/4_PRS/merged.prs.renamed.vcf.gz /home/mkato/hdd_data/0_4_analysis/4_PRS/merged.prs.vcf.gz
bcftools index -t /home/mkato/hdd_data/0_4_analysis/4_PRS/merged.prs.renamed.vcf.gz
