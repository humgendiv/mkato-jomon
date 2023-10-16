import os

#sample_list = ["FM020", "F23_1to8"]
#sample_list = ["F23_9to22",] 
#sample_list = ["I4",]
sample_list = ["T5",]

DIR = "/home/mkato/hdd_data/data/0-2-plink"

for sample in sample_list:
    # 入力ファイルを開く
    input_file = f"{DIR}/{sample}.bim"
    output_file = f"{DIR}/{sample}.tmp.bim"
    with open(input_file, "r") as infile:
        # 出力ファイルを開く
        with open(output_file, "w") as outfile:
            # 入力ファイルの各行について
            for line in infile:
                # タブ区切りで分割
                parts = line.strip().split("\t")

                # 1列目と4列目を取得して新しいIDを作成
                new_id = f"{parts[0]}:{parts[3]}"

                # 2列目を新しいIDで置き換え
                parts[1] = new_id

                # 更新された行を出力ファイルに書き込む
                outfile.write("\t".join(parts) + "\n")

    # 元のファイルを削除
    os.remove(input_file)

    # 一時ファイルを元のファイル名にリネーム
    os.rename(output_file, input_file)