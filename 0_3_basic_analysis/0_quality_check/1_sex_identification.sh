#!/bin/bash

# 出力ファイルの準備
output_file="sex_determination_results.txt"
echo -e "Sample_ID\tBAM_Path\tX_reads\tY_reads\tTotal_XY\tRY_index\tSex" > $output_file

# エラーログファイル
error_log="sex_determination_errors.log"
> $error_log

# BAMファイルパスを読み込んで処理
while IFS= read -r line; do
    # コメント行とか空行をスキップ
    if [[ $line =~ ^#.*$ ]] || [[ -z "$line" ]]; then
        # コメント行からサンプル名を抽出（オプション）
        if [[ $line =~ ^#[[:space:]]+(.+)$ ]]; then
            current_sample_name="${BASH_REMATCH[1]}"
        fi
        continue
    fi
    
    bam_path="$line"
    
    # ファイルの存在確認
    if [ ! -f "$bam_path" ]; then
        echo "ERROR: File not found - $bam_path" >> $error_log
        continue
    fi
    
    # サンプル名の抽出（ファイル名から）
    sample=$(basename "$bam_path" .bam)
    
    # コメント行で指定されたサンプル名があればそちらを使用
    if [ ! -z "$current_sample_name" ]; then
        sample="$current_sample_name"
        current_sample_name=""  # リセット
    fi
    
    echo "Processing: $sample ($bam_path)"
    
    # インデックスの確認・作成
    if [ ! -f "${bam_path}.bai" ] && [ ! -f "${bam_path%.*}.bai" ]; then
        echo "Creating index for $bam_path"
        samtools index "$bam_path" 2>> $error_log
        if [ $? -ne 0 ]; then
            echo "ERROR: Failed to create index for $bam_path" >> $error_log
            continue
        fi
    fi
    
    # idxstatsを実行
    temp_idxstats="${sample}_idxstats_temp.txt"
    samtools idxstats "$bam_path" > "$temp_idxstats" 2>> $error_log
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to run idxstats for $bam_path" >> $error_log
        continue
    fi
    
    # X/Y染色体のリード数を取得（X, chrX, Y, chrYの両方に対応）
    X_reads=$(grep -E "^(X|chrX)\s" "$temp_idxstats" | awk '{sum += $3} END {print sum+0}')
    Y_reads=$(grep -E "^(Y|chrY)\s" "$temp_idxstats" | awk '{sum += $3} END {print sum+0}')
    
    # 合計リード数
    total_XY=$((X_reads + Y_reads))
    
    # RY indexを計算
    if [ $total_XY -gt 0 ]; then
        RY_index=$(echo "scale=6; $Y_reads / $total_XY" | bc)
        
        # 性別判定（Skoglund et al. 2013の基準）
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
    
    # 結果を出力
    echo -e "$sample\t$bam_path\t$X_reads\t$Y_reads\t$total_XY\t$RY_index\t$sex" >> $output_file
    
    # 一時ファイルを削除
    rm -f "$temp_idxstats"
    
done < bam_path_no_problem.txt

echo "Analysis completed. Results saved to: $output_file"
echo "Any errors logged to: $error_log"

# 結果のサマリーを表示
echo -e "\n=== Summary ==="
echo "Total samples processed: $(tail -n +2 $output_file | wc -l)"
echo "Male: $(grep -c "Male$" $output_file)"
echo "Female: $(grep -c "Female$" $output_file)"
echo "Undetermined: $(grep -c "Undetermined$" $output_file)"
echo "No XY reads: $(grep -c "No_XY_reads$" $output_file)"

# 結果を見やすく表示
echo -e "\n=== Results ==="
column -t -s $'\t' $output_file