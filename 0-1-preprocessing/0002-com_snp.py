import os
from multiprocessing import Pool

# 入力ファイルのパス
bim_files = [
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/F23.chr1-7.bim",
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/F23.chr8-22.bim",
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/FM020.chr1-7.bim",
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/FM020.chr8-22.bim",
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/Iyai4b.chr1-7.bim",
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/Iyai4b.chr8-22.bim",
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/Todo5.chr1-7.bim",
    "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/Todo5.chr8-22.bim"
]

# 出力ディレクトリを作成
output_dir = "/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/snp"
os.makedirs(output_dir, exist_ok=True)

def process_bim_file(bim_file):
    print(f"Processing {bim_file}")
    sample = os.path.basename(bim_file).split(".")[0]
    chr_pos_dict = {}
    with open(bim_file, "r") as f:
        for line in f:
            chr_num, pos = line.strip().split()[0], line.strip().split()[3]
            if chr_num not in chr_pos_dict:
                chr_pos_dict[chr_num] = []
            chr_pos_dict[chr_num].append(pos)
    for chr_num, pos_list in chr_pos_dict.items():
        with open(f"{output_dir}/{chr_num}.{sample}.pos", "w") as out_f:
            out_f.write("\n".join(pos_list) + "\n")
            print(f"{chr_num}.{sample}.pos is created")
    print(f"{bim_file} is done")

def process_chr(chr_num):
    print(f"Processing chr{chr_num}")
    samples = ["F23", "FM020", "Iyai4b", "Todo5"]
    pos_sets = []
    for sample in samples:
        with open(f"{output_dir}/{chr_num}.{sample}.pos", "r") as f:
            pos_sets.append(set(f.read().splitlines()))
    print(f"chr{chr_num} is read")
    common_pos = set.intersection(*pos_sets)
    print(f"chr{chr_num} is intersected")
    with open(f"{output_dir}/chr{chr_num}.common.pos", "w") as out_f:
        out_f.write("\n".join(common_pos))
    print(f"chr{chr_num}.common.pos is created")

# 各bimファイルに書かれているIDを染色体ごとに分割（並行実行）
#for bim_file in bim_files:
#    process_bim_file(bim_file)

# 各サンプルで同一染色体のファイルを統合し、全てのサンプルで存在しているポジションのみを書く（並行実行）
for i in range(2, 5):
    process_chr(str(i))

# 4サンプルで統合された22ファイルを統合し、IDの書式に戻す
print("Creating common_snps.txt")
with open(f"{output_dir}/common_snps.txt", "w") as out_f:
    for chr_num in range(1, 23):
        with open(f"{output_dir}/chr{chr_num}.common.pos", "r") as f:
            for pos in f:
                out_f.write(f"{chr_num}:{pos.strip()}\n")

