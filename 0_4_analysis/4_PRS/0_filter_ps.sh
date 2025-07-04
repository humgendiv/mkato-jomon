#!/bin/bash
# Step 2: 1240K SNP抽出（改良版）
set -euo pipefail

INPUT_DIR="/home/mkato/hdd_data/0_1_vcf/chr_removed_bgzip"
OUTPUT_DIR="/home/mkato/hdd_data/0_4_analysis/4_PRS/filtered_prs"
REGION_SRC="/home/mkato/hdd_data/2-2-polygenic/unique_snps.txt"
REGION_FILE="/home/mkato/hdd_data/2-2-polygenic/unique_snps.regions"

# 出力ディレクトリ作成
mkdir -p "$OUTPUT_DIR"

# 1240K.bim から "染色体\t位置" の2列リージョンリストを作成
# ・空行やコメント行を除去
# ・posは数字のみ許可
awk -F':' '$1!~/^#/ && $2 ~ /^[0-9]+$/ { print $1 "\t" $2 }' "$REGION_SRC" \
  | sort -k1,1 -k2,2n \
  | uniq > "$REGION_FILE"

echo "[INFO] Generated region file "$REGION_FILE" with $(wc -l < "$REGION_FILE") sites."

# 並列実行で各VCFをフィルタリング
for vcf in "$INPUT_DIR"/*.vcf.gz; do
  (
    base=$(basename "$vcf")
    echo "[FILTER] Extracting $(grep -c '^[^[:space:]]' "$REGION_FILE") sites from $base"
    bcftools view -R "$REGION_FILE" -v snps -Oz -o "$OUTPUT_DIR/$base" "$vcf"
    echo "[DONE] $base -> $OUTPUT_DIR/$base (variants: $(bcftools view -H "$OUTPUT_DIR/$base" | wc -l))"
  ) &
done

# 全ジョブ完了まで待機
wait

echo "All prs filters completed. Outputs in $OUTPUT_DIR"
