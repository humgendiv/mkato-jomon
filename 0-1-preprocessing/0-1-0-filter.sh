bcftools filter -e 'INFO/DP<10 || INFO/DP>79' -o filtered3.vcf filtered2.vcf
