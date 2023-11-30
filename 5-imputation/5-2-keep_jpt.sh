suffix=".phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz" ;
dir=/home/mkato/hdd_data/data/Genomes1000/vcf/
outdir=/home/mkato/hdd_data/data/Genomes1000/jptvcf

bcftools view --force-samples -S /home/mkato/mkato-jomon/5-imputation/sample_ids.txt \
${dir}/ALL.chr${chr}${suffix} | /usr/local/bin/bgzip -c > ${outdir}/chr${chr}_jpt.vcf.gz

/usr/local/bin/tabix ${outdir}/chr${chr}_jpt.vcf.gz