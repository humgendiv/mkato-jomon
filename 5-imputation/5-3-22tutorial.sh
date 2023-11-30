# CHR変数は、処理する染色体番号を設定します。ここでは1から22までを指定する必要があります。

# 以下のコマンドは、指定された染色体のVCFファイルに対して実行されます。
# '/home/mkato/hdd_data/data/Genomes1000/vcf/chr${CHR}_jpt.vcf.gz' はあなたのVCFファイルのパスに置き換えてください。
bcftools norm -m -any /home/mkato/hdd_data/data/Genomes1000/jptvcf/chr${CHR}_jpt.vcf.gz -Ou |
bcftools view -m 2 -M 2 -v snps -Ob -o /home/mkato/hdd_data/data/Genomes1000/reference_panel/1000GP.chr${CHR}.bcf
bcftools index -f /home/mkato/hdd_data/data/Genomes1000/reference_panel/1000GP.chr${CHR}.bcf