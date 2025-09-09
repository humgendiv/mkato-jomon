#!/bin/bash
# sex_determination_no_index.sh
# 大きなBAMファイルに対してインデックスなしで性別判定

output_file="sex_determination_results.txt"
echo -e "Sample_ID\tBAM_Path\tFile_Size\tX_reads\tY_reads\tTotal_XY\tRY_index\tSex\tProcessing_time" > $output_file

# ログファイル
log_file="sex_determination_log.txt"
> $log_file

# bam_path.txtから読み込み
while IFS= read -r line; do
    # コメント行からサンプル名を抽出
    if [[ $line =~ ^#[[:space:]]+(.+)$ ]]; then
        current_sample_name="${BASH_REMATCH[1]}"
        continue
    fi
    
    [[ -z "$line" ]] && continue
    
    bam_path="$line"
    
    # ファイル存在確認
    if [ ! -f "$bam_path" ]; then
        echo "ERROR: File not found - $bam_path" | tee -a $log_file
        continue
    fi
    
    # サンプル名の決定
    if [ ! -z "$current_sample_name" ]; then
        sample="$current_sample_name"
        current_sample_name=""
    else
        sample=$(basename "$bam_path" .bam)
    fi
    
    # ファイルサイズ取得
    file_size=$(du -h "$bam_path" | cut -f1)
    
    echo "Processing: $sample (Size: $file_size)" | tee -a $log_file
    start_time=$(date +%s)
    
    # X/Y染色体のリード数をカウント
    # -c オプションでカウントのみ（高速）
    # -@ で並列処理
    echo "  Counting X chromosome reads..." | tee -a $log_file
    X_reads=0
    for chr in X chrX; do
        count=$(samtools view -@ 8 -c "$bam_path" "$chr" 2>/dev/null || echo 0)
        X_reads=$((X_reads + count))
    done
    
    echo "  Counting Y chromosome reads..." | tee -a $log_file
    Y_reads=0
    for chr in Y chrY; do
        count=$(samtools view -@ 8 -c "$bam_path" "$chr" 2>/dev/null || echo 0)
        Y_reads=$((Y_reads + count))
    done
    
    total_XY=$((X_reads + Y_reads))
    
    # RY index計算と性別判定
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
    
    # 結果を記録
    result_line="$sample\t$bam_path\t$file_size\t$X_reads\t$Y_reads\t$total_XY\t$RY_index\t$sex\t${processing_time}s"
    echo -e "$result_line" >> $output_file
    
    echo "  Result: X=$X_reads, Y=$Y_reads, RY_index=$RY_index, Sex=$sex (Time: ${processing_time}s)" | tee -a $log_file
    echo "" | tee -a $log_file
    
done < bam_path.txt

# 結果のサマリー
echo "=== Summary ===" | tee -a $log_file
echo "Results saved to: $output_file" | tee -a $log_file

# 結果を表示
echo -e "\n=== Results ===" | tee -a $log_file
column -t -s $'\t' $output_file | tee -a $log_file

# 性別ごとのカウント
echo -e "\n=== Sex Distribution ===" | tee -a $log_file
tail -n +2 $output_file | cut -f8 | sort | uniq -c | tee -a $log_file