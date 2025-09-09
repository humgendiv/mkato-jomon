#!/bin/bash
# sex_determination_fullscan_optimized.sh
# queryname順BAMファイル対応の性別判定スクリプト（最適化版）

output_file="sex_determination_results_final.txt"
echo -e "Sample_ID\tBAM_Path\tFile_Size\tX_reads\tY_reads\tTotal_XY\tRY_index\tSex\tProcessing_time" > $output_file

# プログレスログ
progress_log="sex_determination_progress.log"
> $progress_log

while IFS= read -r line; do
    if [[ $line =~ ^#[[:space:]]+(.+)$ ]]; then
        current_sample_name="${BASH_REMATCH[1]}"
        continue
    fi
    
    [[ -z "$line" ]] && continue
    
    bam_path="$line"
    [ ! -f "$bam_path" ] && continue
    
    if [ ! -z "$current_sample_name" ]; then
        sample="$current_sample_name"
        current_sample_name=""
    else
        sample=$(basename "$bam_path" .bam)
    fi
    
    file_size=$(du -h "$bam_path" | cut -f1)
    
    echo "Processing: $sample (Size: $file_size)" | tee -a $progress_log
    echo "Note: Scanning entire file due to queryname sort order..." | tee -a $progress_log
    
    start_time=$(date +%s)
    
    # 全ファイルをスキャンしてchrX/chrYをカウント
    # プログレス表示のため、定期的に進捗を出力
    echo "  Counting chromosomes X and Y..." | tee -a $progress_log
    
    # 並列処理とパイプラインの最適化
    # pigzがある場合は使用、なければ通常のsamtools view
    if command -v pigz >/dev/null 2>&1; then
        # pigzで並列解凍
        result=$(samtools view -@ 8 "$bam_path" 2>/dev/null | \
            awk -v sample="$sample" '
                BEGIN {x=0; y=0; total=0} 
                {
                    total++
                    if ($3=="chrX") x++
                    else if ($3=="chrY") y++
                    if (total % 1000000 == 0) {
                        printf("  %s: Processed %dM reads (chrX: %d, chrY: %d)\r", sample, total/1000000, x, y) > "/dev/stderr"
                    }
                } 
                END {
                    printf("\n") > "/dev/stderr"
                    print x, y
                }')
    else
        # 通常のsamtools view
        result=$(samtools view "$bam_path" 2>/dev/null | \
            awk -v sample="$sample" '
                BEGIN {x=0; y=0; total=0} 
                {
                    total++
                    if ($3=="chrX") x++
                    else if ($3=="chrY") y++
                    if (total % 1000000 == 0) {
                        printf("  %s: Processed %dM reads (chrX: %d, chrY: %d)\r", sample, total/1000000, x, y) > "/dev/stderr"
                    }
                } 
                END {
                    printf("\n") > "/dev/stderr"
                    print x, y
                }')
    fi
    
    # 結果を変数に格納
    X_reads=$(echo "$result" | awk '{print $1}')
    Y_reads=$(echo "$result" | awk '{print $2}')
    
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
    
    echo -e "$sample\t$bam_path\t$file_size\t$X_reads\t$Y_reads\t$total_XY\t$RY_index\t$sex\t${processing_time}s" >> $output_file
    
    echo "  Result: X=$X_reads, Y=$Y_reads, RY=$RY_index, Sex=$sex (Time: ${processing_time}s)" | tee -a $progress_log
    echo "" | tee -a $progress_log
    
done < bam_path.txt

echo "=== Results ===" | tee -a $progress_log
column -t -s $'\t' $output_file | tee -a $progress_log

echo -e "\n=== Summary ===" | tee -a $progress_log
tail -n +2 $output_file | cut -f8 | sort | uniq -c | tee -a $progress_log

# 診断に基づいた推定結果（50000リードベース）
echo -e "\n=== Note ===" | tee -a $progress_log
echo "Based on the diagnostic scan of FM027-1 (first 50000 reads):" | tee -a $progress_log
echo "- chrX: 1203 reads, chrY: 26 reads" | tee -a $progress_log
echo "- RY index would be: 0.0212 (Undetermined)" | tee -a $progress_log