import os
import gzip

# PRSフォルダのパス
prs_folder = "/home/mkato/hdd_data/data/PS/PRS"

# 出力フォルダのパス
output_folder = "/home/mkato/hdd_data/data/PS/PRS_processed"

# 出力フォルダが存在しない場合は作成する
os.makedirs(output_folder, exist_ok=True)

# PRSフォルダ内のすべてのファイルを処理する
for filename in os.listdir(prs_folder):
    if filename.endswith(".txt.gz"):
        input_path = os.path.join(prs_folder, filename)
        output_path = os.path.join(output_folder, filename[:-3])  # 出力ファイル名から'.gz'を除去

        with gzip.open(input_path, "rt") as input_file, open(output_path, "w") as output_file:
            header = input_file.readline().strip().split()

            # 必要な列のインデックスを取得
            if "P_BOLT" in header:
                p_index = header.index("P_BOLT")
            else:
                p_index = header.index("P")

            chr_index = header.index("CHR")
            pos_index = header.index("POS")
            ref_index = header.index("REF")
            alt_index = header.index("ALT")
            beta_index = header.index("BETA")

            # 出力ファイルのヘッダーを書き込む
            output_file.write("ID\tCHR\tPOS\tREF\tALT\tBETA\tP\n")

            # 各行を処理する
            for line in input_file:
                fields = line.strip().split()
                p_value = float(fields[p_index])

                if p_value <= 0.01:
                    chr_value = fields[chr_index]
                    pos_value = fields[pos_index]
                    ref_value = fields[ref_index]
                    alt_value = fields[alt_index]
                    beta_value = fields[beta_index]

                    # 新しいIDを作成
                    new_id = f"{chr_value}:{pos_value}"

                    # 処理された行を出力ファイルに書き込む
                    output_file.write(f"{new_id}\t{chr_value}\t{pos_value}\t{ref_value}\t{alt_value}\t{beta_value}\t{p_value}\n")
