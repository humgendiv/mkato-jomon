#!/bin/bash
# create_xy_subset.sh
# X/Y染色体のみの小さなBAMファイルを作成

while IFS= read -r line; do
    [[ $line =~ ^#.*$ ]] || [[ -z "$line" ]] && continue
    
    bam_path="$line"
    [ ! -f "$bam_path" ] && continue
    
    output_dir="xy_subset_bams"
    mkdir -p "$output_dir"
    
    basename=$(basename "$bam_path" .bam)
    xy_bam="${output_dir}/${basename}_XY.bam"
    
    echo "Extracting X/Y chromosomes from: $bam_path"
    
    # X/Y染色体のみを抽出（並列処理で高速化）
    samtools view -b -@ 8 "$bam_path" X Y chrX chrY > "$xy_bam"
    
    # 小さなファイルなので、ソートとインデックス作成は速い
    samtools sort -@ 8 -o "${xy_bam}.sorted.bam" "$xy_bam"
    samtools index "${xy_bam}.sorted.bam"
    
    # 元の一時ファイルを削除
    rm "$xy_bam"
    
done < bam_path.txt