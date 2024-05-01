import os

# サンプル名のリスト
samples = ['F23', 'FM020', 'Iyai4b', 'Todo5']

# 共通の遺伝子座を格納するセット
common_loci = set()

# 各サンプルについて処理
for sample in samples:
    # サンプルの遺伝子座を格納するセット
    sample_loci = set()

    # 分割されたbimファイルを読み込む
    for i in range(1, 3):
        file_name = f"/home/mkato/hdd_data/data/0-3-extract_plink/{sample}.chr{1 if i == 1 else 8}-{7 if i == 1 else 22}.bim"
        with open(file_name, 'r') as f:
            for line in f:
                locus = line.split()[1]
                sample_loci.add(locus)

    # 最初のサンプルの場合、共通の遺伝子座に追加
    if len(common_loci) == 0:
        common_loci = sample_loci
    else:
        # 他のサンプルの場合、共通の遺伝子座との積集合を取る
        common_loci = common_loci.intersection(sample_loci)

# 1240K.bimを読み込む
with open("/home/mkato/hdd_data/data/bim/1240K.bim", 'r') as f:
    bim_1240 = set(line.strip() for line in f)

intersection_loci = sorted(common_loci.intersection(bim_1240))

with open('/home/mkato/hdd_data/data/bim/1240K_downsized_jomon.bim', 'w') as f:
    for locus in intersection_loci:
        f.write(locus + '\n')
