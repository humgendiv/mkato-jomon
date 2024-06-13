import pysam

def analyze_cigar_strings(bam_file):
    # CIGAR文字列のパターンと行数を保存する辞書
    cigar_patterns = {}

    # BAMファイルを開く
    with pysam.AlignmentFile(bam_file, "rb") as bamfile:
        # 各リードについてループ
        for read in bamfile:
            cigar_string = read.cigarstring

            # 2SXM2S (Xは任意の整数) のパターンにマッチするかチェック
            if cigar_string.startswith("2S") and cigar_string.endswith("2S") and "M" in cigar_string and len(cigar_string) == 6:
                cigar_pattern = "2SXM2S"
            else:
                cigar_pattern = cigar_string

            # 辞書にCIGAR文字列のパターンと行数を記録
            if cigar_pattern not in cigar_patterns:
                cigar_patterns[cigar_pattern] = 1
            else:
                cigar_patterns[cigar_pattern] += 1

    return cigar_patterns

# BAMファイルのパスを指定
bam_file = "/home1/mkato/hdd_data/data/bam/share/T5_p1_p2_p3.bam"

# CIGAR文字列を解析
cigar_patterns = analyze_cigar_strings(bam_file)


output_file = "./cigar_patterns.txt"
with open(output_file, "w") as f:
    for pattern, count in cigar_patterns.items():
        f.write(f"{pattern}: {count} reads\n")
