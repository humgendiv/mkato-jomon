#!/bin/bash
# detailed_diagnosis.sh
# BAMファイルの詳細診断

# 最初のBAMファイルを使ってテスト
first_bam="/home/mkato/hdd_data/data/sample_data/FM027/FM027-1_DS_PG0301_005_dedup.clip2.sorted.bam"

if [ ! -f "$first_bam" ]; then
    echo "BAM file not found: $first_bam"
    exit 1
fi

echo "Testing with: $(basename $first_bam)"
echo "============================================"

# 1. ヘッダーの確認
echo -e "\n1. Header check for chrX/chrY:"
samtools view -H "$first_bam" 2>/dev/null | grep -E "^@SQ.*SN:chr[XY]" | head -5

# 2. インデックスの状態確認
echo -e "\n2. Checking if index exists:"
ls -la "${first_bam}.bai" 2>/dev/null || ls -la "${first_bam%.*}.bai" 2>/dev/null || echo "No index file found"

# 3. 全染色体のマップ状況を確認（最初の10000リード）
echo -e "\n3. Chromosome distribution (first 10000 reads):"
samtools view "$first_bam" 2>/dev/null | head -10000 | cut -f3 | sort | uniq -c | sort -nr | head -10

# 4. chrXに実際にリードがあるか確認（最初の数行）
echo -e "\n4. Checking if any reads map to chrX (first attempt):"
samtools view "$first_bam" chrX 2>&1 | head -3

# 5. エラーメッセージを詳しく確認
echo -e "\n5. Testing samtools view with chrX (with stderr):"
samtools view "$first_bam" chrX 2>&1 | head -1

# 6. 代替アプローチ：全リードをスキャンしてchrX/chrYを探す
echo -e "\n6. Scanning for chrX/chrY reads in the file:"
echo -n "Scanning first 50000 reads for chrX: "
samtools view "$first_bam" 2>/dev/null | head -50000 | awk '$3=="chrX"' | wc -l
echo -n "Scanning first 50000 reads for chrY: "
samtools view "$first_bam" 2>/dev/null | head -50000 | awk '$3=="chrY"' | wc -l

# 7. BAMファイルの形式を確認
echo -e "\n7. Checking BAM file format:"
samtools quickcheck "$first_bam" && echo "BAM file format is valid" || echo "BAM file format may have issues"

# 8. フラグ統計を確認
echo -e "\n8. General statistics:"
samtools flagstat "$first_bam" 2>&1 | head -10