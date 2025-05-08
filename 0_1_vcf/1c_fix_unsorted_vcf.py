#!/usr/bin/env python3
# VCFファイルからPOS順序違反の行を検出し削除して新ファイルを作成

import gzip
from pathlib import Path

input_path = Path("/home/mkato/hdd_data/0_1_vcf/chr_removed_bgzip/I4.vcf.gz")
output_path = input_path.with_name(input_path.stem + ".fixed.vcf.gz")

prev_chrom = None
prev_pos = -1
skipped_lines = 0

with gzip.open(input_path, "rt") as infile, gzip.open(output_path, "wt") as outfile:
    for lineno, line in enumerate(infile, start=1):
        if line.startswith("#"):
            outfile.write(line)
            continue

        parts = line.strip().split("\t")
        if len(parts) < 2:
            continue

        chrom = parts[0]
        try:
            pos = int(parts[1])
        except ValueError:
            continue

        if chrom == prev_chrom and pos < prev_pos:
            skipped_lines += 1
            print(f"[SKIP] Line {lineno}: POS {pos} after {prev_pos} in {chrom}")
            continue  # 順序違反 → 書き込まない

        outfile.write(line)
        prev_chrom = chrom
        prev_pos = pos

print(f"[DONE] Fixed VCF written to: {output_path}")
print(f"[INFO] Total skipped unsorted lines: {skipped_lines}")
