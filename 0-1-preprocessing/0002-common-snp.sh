#!/bin/bash

# 入力ファイルのパス
bim_files=(
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/F23.chr1-7.bim"
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/F23.chr8-22.bim"
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/FM020.chr1-7.bim"
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/FM020.chr8-22.bim"
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/Iyai4b.chr1-7.bim"
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/Iyai4b.chr8-22.bim"
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/Todo5.chr1-7.bim"
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/Todo5.chr8-22.bim"
)

# 出力ディレクトリを作成
output_dir="/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/snp"
mkdir -p "${output_dir}"

# 各bimファイルに書かれているIDを染色体ごとに分割（並行実行）
parallel --j 8 'sample=$(basename {} | cut -d"." -f1); awk "{print \$4 > \"'${output_dir}'/\${sample}.\"\$1\".pos\"}" {}' ::: "${bim_files[@]}"

# 各サンプルで同一染色体のファイルを統合し、全てのサンプルで存在しているポジションのみを書く（並行実行）
parallel --j 22 'join -a1 -a2 -o1.1 "'${output_dir}'/F23.{}.pos" "'${output_dir}'/FM020.{}.pos" | join -a1 -a2 -o1.1 - "'${output_dir}'/Iyai4b.{}.pos" | join -a1 -a2 -o1.1 - "'${output_dir}'/Todo5.{}.pos" > "'${output_dir}'/chr{}.common.pos"' ::: {1..22}

# 4サンプルで統合された22ファイルを統合し、IDの書式に戻す
for chr in {1..22}; do
    awk '{print "'${chr}':"$0}' "${output_dir}/chr${chr}.common.pos" >> "${output_dir}/common_snps.txt"
done

# 一時ファイルを削除
rm "${output_dir}"/*.pos
