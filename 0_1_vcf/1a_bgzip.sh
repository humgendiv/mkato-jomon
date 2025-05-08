#!/bin/bash

INPUT_DIR="/home/mkato/hdd_data/0_1_vcf/chr_removed"
OUTPUT_DIR="/home/mkato/hdd_data/0_1_vcf/chr_removed_bgzip"

mkdir -p "$OUTPUT_DIR"

for file in "$INPUT_DIR"/*.vcf.gz; do
  (
    base=$(basename "$file")
    echo "[START] Recompressing $base..."
    gunzip -c "$file" | bgzip -c > "$OUTPUT_DIR/$base"
    echo "[DONE] $base -> $OUTPUT_DIR/$base"
  ) &
done

wait
echo "[ALL DONE] All files bgzipped in parallel to $OUTPUT_DIR"
