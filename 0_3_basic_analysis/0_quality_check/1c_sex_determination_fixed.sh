#!/bin/bash
# sex_determination_fixed.sh
# chrX/chrYに対応した修正版

output_file="sex_determination_results.txt"
echo -e "Sample_ID\tBAM_Path\tFile_Size\tX_reads\tY_reads\tTotal_XY\tRY_index\tSex\tProcessing_time" > $output_file

# デバッグ用ログ
debug_log="sex_determination_debug.log"
> $debug_log

while IFS= read -r line; do
    # コメント行からサンプル名を抽出
    if [[ $line =~ ^#[[:space:]]+(.+)$ ]]; then
        current_sample_name="${BASH_REMATCH[1]}"
        continue
    fi
    
    [[ -z "$line" ]] && continue
    
    bam_path="$line"
    
    if [ ! -f "$bam_path" ]; then
        echo "ERROR: File not found - $bam_path" >> $debug_log
        continue
    fi
    
    # サンプル名の決定
    if [ ! -z "$current_sample_name" ]; then
        sample="$current_sample_name"
        current_sample_name=""
    else
        sample=$(basename "$bam_path" .bam)
    fi
    
    # ファイルサイズ
    file_size=$(du -h "$bam_path" | cut -f1)
    
    echo "Processing: $sample (Size: $file_size)"
    echo "BAM file: $bam_path" >> $debug_log
    
    start_time=$(date +%s)
    
    # まずヘッダーで染色体の存在を確認
    echo "Checking header for chrX/chrY..." >> $debug_log
    samtools view -H "$bam_path" 2>/dev/null | grep -E "^@SQ.*SN:chr[XY]" >> $debug_log
    
    # chrXのカウント（デバッグ情報付き）
    echo "  Counting chrX reads..."
    echo "Running: samtools view -c $bam_path chrX" >> $debug_log
    X_reads=$(samtools view -c "$bam_path" chrX 2>&1)
    
    # エラーチェック
    if [[ "$X_reads" =~ "error" ]] || [[ "$X_reads" =~ "fail" ]]; then
        echo "Error counting chrX: $X_reads" >> $debug_log
        X_reads=0
    else
        echo "chrX count: $X_reads" >> $debug_log
    fi
    
    # chrYのカウント
    echo "  Counting chrY reads..."
    echo "Running: samtools view -c $bam_path chrY" >> $debug_log
    Y_reads=$(samtools view -c "$bam_path" chrY 2>&1)
    
    # エラーチェック
    if [[ "$Y_reads" =~ "error" ]] || [[ "$Y_reads" =~ "fail" ]]; then
        echo "Error counting chrY: $Y_reads" >> $debug_log
        Y_reads=0
    else
        echo "chrY count: $Y_reads" >> $debug_log
    fi
    
    # 数値変換（念のため）
    X_reads=$(echo "$X_reads" | grep -oE '^[0-9]+' || echo 0)
    Y_reads=$(echo "$Y_reads" | grep -oE '^[0-9]+' || echo 0)
    
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
    
    result_line="$sample\t$bam_path\t$file_size\t$X_reads\t$Y_reads\t$total_XY\t$RY_index\t$sex\t${processing_time}s"
    echo -e "$result_line" >> $output_file
    
    echo "  Result: X=$X_reads, Y=$Y_reads, RY_index=$RY_index, Sex=$sex (Time: ${processing_time}s)"
    echo "----------------------------------------" >> $debug_log
    echo ""
    
done < bam_path.txt

echo "=== Results ==="
column -t -s $'\t' $output_file

echo -e "\n=== Summary ==="
tail -n +2 $output_file | cut -f8 | sort | uniq -c

echo -e "\nDebug log saved to: $debug_log"