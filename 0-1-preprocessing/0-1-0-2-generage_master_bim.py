unique_positions = set()

# 最初のファイルを読む
with open("/home/mkato/hdd_data/data/bim/1240K.bim", "r") as f1:
    for line in f1:
        unique_positions.add(line.strip())

# 2番目のファイルを読む
with open("/home/mkato/hdd_data/data/bim/array_ID_ken.txt", "r") as f2:
    for line in f2:
        unique_positions.add(line.strip())

# 3番目のファイルを読む
#with open("/home/mkato/hdd_data/data/PS/unique_snps.txt", "r") as f3:
#    for line in f3:
#        unique_positions.add(line.strip())

# 結果を出力
with open("/home/mkato/hdd_data/data/bim/merged_positions.bim", "w") as out_f:
    for pos in sorted(unique_positions):
        out_f.write(f"{pos}\n")
