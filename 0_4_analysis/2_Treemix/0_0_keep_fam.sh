plink --bfile /home/mkato/hdd_data/0_2_1240K/merged_with_1240K \
    --keep-fam /home/mkato/mkato-jomon/0_4_analysis/2_Treemix/targetpops.txt   --make-bed \
    --maf 0.01 \
  --out /home/mkato/hdd_data/0_4_analysis/2_Treemix/merged_with_1240K.targetpops

plink --bfile /home/mkato/hdd_data/0_4_analysis/2_Treemix/merged_with_1240K.targetpops \
    --recode vcf bgz \
    --out /home/mkato/hdd_data/0_4_analysis/2_Treemix/merged_with_1240K.targetpops