#!/usr/bin/env python3
# Step 1: chr除去 + 拡張子統一 + 元ファイル退避 + ログ出力
from pathlib import Path
import gzip
import re
import shutil
from concurrent.futures import ProcessPoolExecutor

input_dir = Path("/home/mkato/hdd_data/0_1_vcf")
output_dir = input_dir / "chr_removed"
output_dir.mkdir(parents=True, exist_ok=True)

# 対象ファイル拡張子
extensions = ["*.vcf.gz", "*.gvcf.gz", "*.g.vcf.gz"]
vcf_files = [p for ext in extensions for p in input_dir.glob(ext) if p.is_file()]

# chr除去関数
def process_chr_removal(input_path):
    output_name = input_path.stem.split('.')[0] + ".vcf.gz"
    output_path = output_dir / output_name

    print(f"[START] Processing: {input_path.name}")

    try:
        with gzip.open(input_path, 'rt') as infile, gzip.open(output_path, 'wt') as outfile:
            for line in infile:
                if line.startswith("#"):
                    line = re.sub(r'chr(\d+|X|Y|MT)', r'\1', line)
                else:
                    line = re.sub(r'^chr(\d+|X|Y|MT)', r'\1', line)
                outfile.write(line)
        print(f"[DONE] chr removed and saved to: {output_path.name}")

    except Exception as e:
        print(f"[ERROR] Failed processing {input_path.name}: {e}")

    return output_path

# 並列実行
with ProcessPoolExecutor() as executor:
    results = list(executor.map(process_chr_removal, vcf_files))
