#!/bin/bash
# FORMAT/AD を削除してマージ用VCFを準備・統合するスクリプト

INPUT_DIR="/home/mkato/hdd_data/0_1_vcf/filtered_1240K"
CLEAN_DIR="/home/mkato/hdd_data/0_1_vcf/filtered_1240K_noAD"
MERGED_VCF="/home/mkato/hdd_data/0_1_vcf/merged.1240K.vcf.gz"

mkdir -p "$CLEAN_DIR"

# 各VCFから FORMAT/AD を削除し、インデックス作成
for file in "$INPUT_DIR"/*.vcf.gz; do
  base=$(basename "$file")
  echo "[PROCESS] Removing FORMAT/AD from $base"
  bcftools annotate -x FORMAT/AD -Oz -o "$CLEAN_DIR/$base" "$file"
  bcftools index -t "$CLEAN_DIR/$base"
done

# マージ処理
echo "[MERGE] Merging all cleaned VCFs..."
bcftools merge -m all -Oz -o "$MERGED_VCF" "$CLEAN_DIR"/*.vcf.gz
bcftools index -t "$MERGED_VCF"

echo "[DONE] Merged VCF with FORMAT/AD removed: $MERGED_VCF"
