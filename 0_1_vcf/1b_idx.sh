#!/bin/bash

INPUT_DIR="/home/mkato/hdd_data/0_1_vcf/chr_removed_bgzip"

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
