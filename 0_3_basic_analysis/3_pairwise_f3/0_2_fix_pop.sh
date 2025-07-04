awk '{
  # $1 が "Mbuti.DG:B_Mbuti-4.DG" のような形式 ⇒ split で ":" 前を取り出す
  split($1, a, ":");
  pop = a[1];
  # 出力：<サンプル名> <性別> <ポップ名>
  printf "%s %s %s\n", $1, $2, pop;
}' \
  /home/mkato/hdd_data/0_3_basic_analysis/3_pairwise_f3/merged_with_1240K.targetpops.ind \
  > /home/mkato/hdd_data/0_3_basic_analysis/3_pairwise_f3/merged_with_1240K.targetpops.ind.fixed
