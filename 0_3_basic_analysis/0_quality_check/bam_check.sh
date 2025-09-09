#!/bin/bash
# quick_bam_check.sh
# 大きなBAMファイルの状態を素早く確認

echo -e "BAM_Path\tSize_GB\tHeader_SO\tIndex_Status\tSample_Sort_Check" > bam_quick_status.txt

while IFS= read -r line; do
    [[ $line =~ ^#.*$ ]] || [[ -z "$line" ]] && continue
    
    bam_path="$line"
    [ ! -f "$bam_path" ] && continue
    
    # ファイルサイズを取得（GB単位）
    size_gb=$(du -h "$bam_path" | cut -f1)
    
    # ヘッダーのみチェック（高速）
    header_so=$(samtools view -H "$bam_path" 2>/dev/null | grep "^@HD" | grep -oP "SO:\K\w+")
    
    # インデックスの存在確認
    index_status="No"
    [ -f "${bam_path}.bai" ] || [ -f "${bam_path%.*}.bai" ] && index_status="Yes"
    
    # 最初の10000リードだけでソート状態を確認
    sort_check=$(samtools view "$bam_path" 2>/dev/null | head -10000 | \
        awk -F'\t' '$3!="*"{print $3"\t"$4}' | \
        awk 'NR>1{if($1==prev_chr && $2<prev_pos){print "Not_sorted"; exit}} {prev_chr=$1; prev_pos=$2} END{print "Appears_sorted"}')
    
    echo -e "$bam_path\t$size_gb\t$header_so\t$index_status\t$sort_check" >> bam_quick_status.txt
done < bam_path.txt

column -t -s $'\t' bam_quick_status.txt