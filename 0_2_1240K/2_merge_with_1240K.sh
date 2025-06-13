plink \
  --bfile /home/mkato/hdd_data/data/AADR/1240K \
  --bmerge /home/mkato/hdd_data/0_2_1240K/jomon_merged \
  --make-bed \
  --out /home/mkato/hdd_data/0_2_1240K/merged_with_1240K


plink \
  --bfile /home/mkato/hdd_data/0_2_1240K/jomon_merged \
  --exclude /home/mkato/hdd_data/0_2_1240K/merged_with_1240K-merge.missnp \
  --make-bed \
  --out /home/mkato/hdd_data/0_2_1240K/jomon_merged.cleaned


plink \
  --bfile /home/mkato/hdd_data/data/AADR/1240K \
  --bmerge /home/mkato/hdd_data/0_2_1240K/jomon_merged.cleaned \
  --make-bed \
  --out /home/mkato/hdd_data/0_2_1240K/merged_with_1240K \
  --allow-no-sex
