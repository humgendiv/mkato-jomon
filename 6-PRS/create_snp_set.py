import os

# 入力ファイルのディレクトリパス
input_dir = "/home/mkato/hdd_data/data/PS/PRS_processed"

# 出力ファイルのパス
output_file = "/home/mkato/hdd_data/data/PS/unique_snps.txt"

# ユニークなSNPを格納するセット
unique_snps = set()

# 入力ディレクトリ内の全ファイルを処理
for filename in os.listdir(input_dir):
    if filename.endswith(".txt"):
        file_path = os.path.join(input_dir, filename)
        
        # ファイルを読み込み、SNPをセットに追加
        with open(file_path, "r") as f:
            next(f)  # ヘッダー行をスキップ
            for line in f:
                fields = line.strip().split("\t")
                snp = f"{fields[1]}:{fields[2]}"  # CHR:POSの形式でSNPを表現
                unique_snps.add(snp)

# ユニークなSNPをリストに変換し、染色体とポジションでソート
sorted_snps = sorted(list(unique_snps), key=lambda x: (int(x.split(":")[0]), int(x.split(":")[1])))

# 出力ファイルに書き込み
with open(output_file, "w") as f:
    for snp in sorted_snps:
        f.write(f"{snp}\n")
