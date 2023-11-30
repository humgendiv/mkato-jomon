prefix="ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/ALL.chr" ;

suffix=".phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz" ;

cd /home/mkato/hdd_data/data/Genomes1000/vcf
wget "${prefix}""${chr}""${suffix}" "${prefix}""${chr}""${suffix}".tbi ;
