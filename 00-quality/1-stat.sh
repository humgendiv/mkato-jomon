#!/bin/bash

# ベースディレクトリを指定
BASE_DIR="/home/mkato/hdd_data/0-genome_data"

# 各サンプルフォルダに対して処理を行う関数
process_vcf() {
    SAMPLE_DIR="$1"
    VCF_FILE=$(find "$SAMPLE_DIR" -maxdepth 1 -name "*.vcf.gz")
    
    if [ -n "$VCF_FILE" ]; then
        echo "Processing $VCF_FILE"
        bcftools stats "$VCF_FILE" > "${SAMPLE_DIR}/stats.txt"
    fi
}

# findでサンプルフォルダを列挙し、xargsで並列処理を行う
export -f process_vcf
find "${BASE_DIR}" -mindepth 1 -maxdepth 1 -type d | xargs -n 1 -P 8 -I {} bash -c 'process_vcf "{}"'
