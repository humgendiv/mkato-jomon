#!/bin/bash

INPUT_DIR="/home/mkato/hdd_data/0_4_analysis/4_PRS/filtered_prs"
NOAD_DIR="/home/mkato/hdd_data/0_4_analysis/4_PRS/filtered_prs_noAD"
CLEAN_DIR="/home/mkato/hdd_data/0_4_analysis/4_PRS/filtered_prs_cleaned"
MERGED_VCF="/home/mkato/hdd_data/0_4_analysis/4_PRS/merged.prs.vcf.gz"

for file in "$INPUT_DIR"/*.vcf.gz; do
  (
    base=$(basename "$file")
    echo "[START] Indexing $base..."
    bcftools index -t "$file"
    echo "[DONE] Indexed $base"
  ) &
done

wait
echo "[ALL DONE] All .vcf.gz files in $INPUT_DIR indexed (.tbi)"

#!/bin/bash
# FORMAT情報と破損・異常REF/ALTを除去してVCFをマージし、IDを"chr:pos"で統一するスクリプト（並列実行対応）



mkdir -p "$NOAD_DIR"
mkdir -p "$CLEAN_DIR"

echo "[STEP 1] Removing FORMAT fields..."
for file in "$INPUT_DIR"/*.vcf.gz; do
  (
    base=$(basename "$file")
    echo "[PROCESS] Removing FORMAT from $base"
    bcftools annotate -x ^FORMAT/GT \
      -Oz -o "$NOAD_DIR/$base" "$file"
    bcftools index -t "$NOAD_DIR/$base"
  ) &
done
wait

echo "[STEP 2] Cleaning malformed REF/ALT entries..."
for file in "$NOAD_DIR"/*.vcf.gz; do
  (
    base=$(basename "$file")
    echo "[CLEAN] Filtering malformed REF/ALT from $base"
    zcat "$file" \
      | awk '!/^#/ && ($4 == "." || $4 ~ /^[0-9]+$/ || $5 ~ /^[0-9]+$/ || split($5, a, ",") > 4) { next } { print }' \
      | bgzip -c > "$CLEAN_DIR/$base"
    bcftools index -t "$CLEAN_DIR/$base"
  ) &
done
wait

echo "[STEP 3] Merging all cleaned VCFs..."
# まずマージを実行して一時ファイルに保存
bcftools merge -m all -Oz -o "$MERGED_VCF.tmp" "$CLEAN_DIR"/*.vcf.gz

# ステップ4: IDをchr:posに統一
echo "[STEP 4] Resetting ID to chr:pos..."
zcat "$MERGED_VCF.tmp" \
  | awk 'BEGIN{OFS="	"} /^#/{print; next} {$3=$1":"$2; print}' \
  | bgzip -c > "$MERGED_VCF"

# インデックス作成
echo "[INDEX] Indexing merged VCF"
bcftools index -t "$MERGED_VCF"

# 一時ファイルの削除
echo "[CLEANUP] Removing temporary file"
rm "$MERGED_VCF.tmp"

echo "[DONE] Merged VCF with cleaned FORMAT, REF/ALT and unified IDs: $MERGED_VCF"
