# 染色体1から22までの各ファイルに対して順番に処理を行います。
# サイトのみを含むVCFファイルを生成します。
bcftools view -G -Oz -o /home/mkato/hdd_data/data/Genomes1000/reference_panel/1000GP.chr${CHR}.sites.vcf.gz /home/mkato/hdd_data/data/Genomes1000/reference_panel/1000GP.chr${CHR}.bcf
# 生成したVCFファイルのインデックスを作成します。
bcftools index -f /home/mkato/hdd_data/data/Genomes1000/reference_panel/1000GP.chr${CHR}.sites.vcf.gz

