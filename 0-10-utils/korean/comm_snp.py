def read_ids(filename):
    with open(filename, 'r') as file:
        return set(line.strip() for line in file)

def write_ids(filename, ids):
    with open(filename, 'w') as file:
        for id_ in sorted(ids):
            file.write(f"{id_}\n")

# ファイル名を指定
file1 = '/home/mkato/hdd_data/data/bim/korean.bim'
file2 = '/home/mkato/hdd_data/data/bim/jomon_full.txt'
output_file = 'jomon_korean_comm.txt'

# 各ファイルからIDを読み込む
ids1 = read_ids(file1)
ids2 = read_ids(file2)

# 共通するIDを抽出
common_ids = ids1 & ids2

# 共通するIDをファイルに書き込む
write_ids(output_file, common_ids)

print(f"共通するIDが {output_file} に書き込まれました。")

