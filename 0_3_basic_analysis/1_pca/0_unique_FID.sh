# ユニークなFIDを抽出
cut -d ' ' -f1 /home/mkato/hdd_data/0_2_1240K/merged_with_1240K.trunc.fam | sort | uniq > /home/mkato/hdd_data/0_3_basic_analysis/1_pca/all_fids.txt

# 元のFIDリスト
FIDLIST=/home/mkato/hdd_data/0_3_basic_analysis/1_pca/all_fids.txt

# 検索語ファイル
CONTAINS=0p_contains.txt
EXACT=0p_exact.txt

# 出力先
OUTFILE=/home/mkato/hdd_data/0_3_basic_analysis/1_pca/target_pops.txt

# 一時ファイル
TMP1=$(mktemp)
TMP2=$(mktemp)

# 部分一致（contains.txt）
grep -iFf "$CONTAINS" "$FIDLIST" > "$TMP1"

# 完全一致（exact.txt）
grep -ixFf "$EXACT" "$FIDLIST" > "$TMP2"

# 結合して重複を除く
cat "$TMP1" "$TMP2" | sort | uniq > "$OUTFILE"

# 終了メッセージ
echo "[INFO] poplist written to $OUTFILE"
