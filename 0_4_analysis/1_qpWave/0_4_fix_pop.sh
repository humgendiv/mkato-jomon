awk '{
  # $1 が "Mbuti.DG:B_Mbuti-4.DG" のような形式 ⇒ split で ":" 前を取り出す
  split($1, a, ":");
  pop = a[1];
  # 出力：<サンプル名> <性別> <ポップ名>
  printf "%s %s %s\n", $1, $2, pop;
}' \
  /home/mkato/hdd_data/0_4_analysis/1_qpWave/merged_outgroup_1240K.ind \
  > /home/mkato/hdd_data/0_4_analysis/1_qpWave/merged_outgroup_1240K.fixed.ind
