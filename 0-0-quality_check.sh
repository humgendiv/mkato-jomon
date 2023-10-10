#!/bin/bash

# bcftools statsを使用して、各VCFファイルの統計情報を取得できます。
# 統計情報には、
# 変異の数、トランジション/トランスバージョン比、欠損データの割合、深度の分布
# などが含まれます
DIR="/home1/mkato/hdd_data/data/0-0-raw_vcf"
OUTPUT_DIR="$DIR/stats"

mkdir -p $OUTPUT_DIR

SAMPLES=("F23" "FM020" "I4" "T5")

for SAMPLE in "${SAMPLES[@]}"
do
    bcftools stats $DIR/${SAMPLE}.vcf.gz > $OUTPUT_DIR/${SAMPLE}_stats.txt
done
