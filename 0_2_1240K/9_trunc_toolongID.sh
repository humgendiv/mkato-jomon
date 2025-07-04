awk '{
  # 合算制限39文字に合わせて分割
  total_limit = 38
  fid = $1
  iid = $2
  rem = total_limit - length(fid)
  if (rem < 1) {
    fid = substr(fid, 1, 32)
    iid = substr(iid, 1, 1)
  } else if (length(iid) > rem) {
    iid = substr(iid, 1, rem)
  }
  print fid, iid, $3, $4, $5, $6
}' /home/mkato/hdd_data/0_2_1240K/merged_with_1240K.fam > /home/mkato/hdd_data/0_2_1240K/merged_with_1240K.trunc.fam

cp /home/mkato/hdd_data/0_2_1240K/merged_with_1240K.bed /home/mkato/hdd_data/0_2_1240K/merged_with_1240K.trunc.bed
cp /home/mkato/hdd_data/0_2_1240K/merged_with_1240K.bim /home/mkato/hdd_data/0_2_1240K/merged_with_1240K.trunc.bim