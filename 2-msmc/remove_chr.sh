#!/bin/bash

# 入力ディレクトリ（適宜書き換え）
input_dir="/home1/mkato/hdd_data/data/2-msmc/FM020_sorted/"
output_dir="${input_dir}/modified_mask_and_vcf"

# 出力先ディレクトリ作成（存在しなければ）
mkdir -p "${output_dir}"

# 対象拡張子
extensions=("*.bed.gz" "*.vcf.gz")

# ループで対象ファイルを処理
for ext in "${extensions[@]}"; do
    for file in "${input_dir}"/${ext}; do
        # ファイルが存在しない場合はスキップ
        [ -e "$file" ] || continue

        filename=$(basename "${file}")
        output_file="${output_dir}/${filename}"

        echo "Processing ${file} -> ${output_file}"

        # chr削除して圧縮
        zcat "${file}" | sed 's/\bchr//g' | bgzip -c > "${output_file}"
    done
done
