#!/bin/bash
# check_chromosome_names.sh
# BAMファイルの染色体名を確認

echo "Checking chromosome names in BAM files..."
echo -e "BAM_File\tChromosome_Names_Sample" > chromosome_names.txt

while IFS= read -r line; do
    [[ $line =~ ^#.*$ ]] || [[ -z "$line" ]] && continue
    
    bam_path="$line"
    [ ! -f "$bam_path" ] && continue
    
    echo "Checking: $(basename $bam_path)"
    
    # ヘッダーから染色体名を取得
    chr_list=$(samtools view -H "$bam_path" 2>/dev/null | grep "^@SQ" | cut -f2 | cut -d: -f2 | tr '\n' ',' | sed 's/,$//')
    
    # または、実際のリードから染色体名を取得（最初の1000リード）
    if [ -z "$chr_list" ]; then
        chr_list=$(samtools view "$bam_path" 2>/dev/null | head -1000 | cut -f3 | sort -u | tr '\n' ',' | sed 's/,$//')
    fi
    
    echo -e "$(basename $bam_path)\t$chr_list" >> chromosome_names.txt
    
    # X/Y染色体に該当しそうな名前を探す
    echo "  Searching for X/Y chromosome patterns..."
    samtools view -H "$bam_path" 2>/dev/null | grep "^@SQ" | grep -iE "(^@SQ.*SN:.*[XY]|chr[XY]|^@SQ.*SN:[XY])" | head -5
    
done < bam_path_no_problem.txt

echo -e "\n=== Chromosome names found ==="
cat chromosome_names.txt