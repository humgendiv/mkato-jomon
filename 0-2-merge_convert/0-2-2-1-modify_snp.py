import os

# SNPファイルのパス
input_file_path = '/home/mkato/hdd_data/data/AADR/v54.1.p1_1240K_public.bim'
# 修正後のSNPファイルの一時保存パス
temp_output_file_path = '/home/mkato/hdd_data/data/AADR/v54.1.p1_1240K_public.new.bim'

# 入力ファイルを開く
with open(input_file_path, 'r') as infile:
    # 出力ファイルを開く
    with open(temp_output_file_path, 'w') as outfile:
        # 各行に対して処理を行う
        for line in infile:
            # 行をタブで分割
            fields = line.strip().split()
            # 染色体番号とポジションを用いて新しいIDを生成
            new_id = f"{fields[0]}:{fields[3]}"
            # 新しいIDを1列目に設定
            fields[1] = new_id
            # 行を再結合して出力
            outfile.write('\t'.join(fields) + '\n')
