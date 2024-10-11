mkdir -p /home1/mkato/hdd_data/2-1-prefectural_conparison/Pruned/jomon

plink --bfile /home1/mkato/hdd_data/1-merged_data/sample/merged/m_merged_jomon \
 --indep 50 5 1.5 --out /home1/mkato/hdd_data/2-1-prefectural_conparison/Pruned/jomon

plink --bfile /home1/mkato/hdd_data/1-merged_data/sample/merged/m_merged_jomon \
 --extract /home1/mkato/hdd_data/2-1-prefectural_conparison/Pruned/jomon.prune.in \
 --make-bed --out /home1/mkato/hdd_data/2-1-prefectural_conparison/Pruned/jomon

plink --bfile /home1/mkato/hdd_data/2-1-prefectural_conparison/Pruned/jomon \
 --recode vcf bgz --out /home1/mkato/hdd_data/2-1-prefectural_conparison/Pruned/jomon