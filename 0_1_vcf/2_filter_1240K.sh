#!/bin/bash
# Step 2: 1240K SNP抽出
INPUT_DIR="/home/mkato/hdd_data/0_1_vcf/chr_removed_bgzip"
OUTPUT_DIR="/home/mkato/hdd_data/0_1_vcf/filtered_1240K"
BED_FILE="/home/mkato/hdd_data/data/bim/1240K_sites.bed"

mkdir -p "$OUTPUT_DIR"

# .bim -> .bed 変換（初回のみでOK）
awk -F: '{print $1"\t"($2-1)"\t"$2}' /home/mkato/hdd_data/data/bim/1240K.bim > "$BED_FILE"

# 並列実行
for vcf in "$INPUT_DIR"/*.vcf.gz; do
  base=$(basename "$vcf")
  bcftools view -R "$BED_FILE" -Oz -o "$OUTPUT_DIR/$base" "$vcf" &
done

wait
echo "All 1240K filters completed."
