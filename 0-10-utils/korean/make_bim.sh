#!/bin/bash

output_file="/home/mkato/hdd_data/data/bim/korean.bim"

# 出力ファイルを初期化
echo -n "" > ${output_file}

# chr1からchr22までのファイルを処理
for i in {1..22}; do
    input_file="/home/mkato/hdd_data/data/Genomes/korean/af/chr${i}.af.txt"
    
    # IDカラムを抽出して出力ファイルに追記
    tail -n +2 ${input_file} | cut -f1 >> ${output_file}
done
