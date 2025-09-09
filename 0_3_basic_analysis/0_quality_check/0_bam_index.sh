#!/bin/bash
# fast_sex_determination.sh
# インデックスなしで性別判定を行う高速版

output_file="sex_determination_fast_results.txt"
echo -e "Sample_ID\tBAM_Path\tX_reads\tY_reads\tTotal_XY\tRY_index\tSex\tProcessing_time" > $output_file

while IFS= read -r line; do
    # コメント行からサンプル名を抽出
    if [[ $line =~ ^#[[:space:]]+(.+)$ ]]; then
        current_sample_name="${BASH_REMATCH[1]}"
        continue
    fi
    
    [[ -z "$line" ]] && continue
    
    bam_path="$line"
    [ ! -f "$bam_path" ] && continue
    
    # サンプル名の決定
    if [ ! -z "$current_sample_name" ]; then
        sample="$current_sample_name"
        current_sample_name=""
    else
        sample=$(basename "$bam_path" .bam)
    fi
    
    echo "Processing: $sample"
    start_time=$(date +%s)
    
    # X/Y染色体のリード数を直接カウント（インデックス不要）
    # 並列処理で高速化
    X_reads=$(samtools view -@ 4 -c "$bam_path" X chrX 2>/dev/null)
    Y_reads=$(samtools view -@ 4 -c "$bam_path" Y chrY 2>/dev/null)
    
    # エラーチェック
    [ -z "$X_reads" ] && X_reads=0
    [ -z "$Y_reads" ] && Y_reads=0
    
    total_XY=$((X_reads + Y_reads))
    
    # RY index計算
    if [ $total_XY -gt 0 ]; then
        RY_index=$(echo "scale=6; $Y_reads / $total_XY" | bc)
        
        if (( $(echo "$RY_index < 0.016" | bc -l) )); then
            sex="Female"
        elif (( $(echo "$RY_index > 0.075" | bc -l) )); then
            sex="Male"
        else
            sex="Undetermined"
        fi
    else
        RY_index="NA"
        sex="No_XY_reads"
    fi
    
    end_time=$(date +%s)
    processing_time=$((end_time - start_time))
    
    echo -e "$sample\t$bam_path\t$X_reads\t$Y_reads\t$total_XY\t$RY_index\t$sex\t${processing_time}s" >> $output_file
    
done < bam_path.txt

echo "Analysis completed. Results saved to: $output_file"