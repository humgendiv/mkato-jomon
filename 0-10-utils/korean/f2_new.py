import pandas as pd
import glob

# VCFファイルのパス
vcf_file = '/home/mkato/hdd_data/data/Genomes/korean/jomon_korean_comm/merged/m_jomon_fullkorean_complete.vcf'

# アリル頻度データのディレクトリ
freq_dir = '/home/mkato/hdd_data/data/Genomes/korean/af/'

# f2統計量を計算する関数
def calculate_f2(vcf_genotype, ref, alt, freq_ref, freq_alt, freq):
    if vcf_genotype == '0/0':
        genotype_value = 0.0
    elif vcf_genotype in {'0/1', '1/0'}:
        genotype_value = 0.5
    elif vcf_genotype == '1/1':
        genotype_value = 1.0
    else:
        return None  # 無効な遺伝子型の場合

    if ref == freq_ref:
        if alt == freq_alt or alt == '.':
            freq_value = freq
        else:
            return None  # 無効なアリルの場合
    elif ref == freq_alt and (alt == freq_ref or alt == '.'):
        freq_value = 1.0 - freq
    else:
        return None  # 無効なアリルの場合

    return (genotype_value - freq_value) ** 2

# VCFファイルをデータフレームとして読み込む
vcf_data = pd.read_csv(vcf_file, sep='\t', comment='#', header=None)
vcf_data.columns = ['CHROM', 'POS', 'ID', 'REF', 'ALT'] + [f'SAMPLE_{i}' for i in range(1, 5)]

# 各染色体のアリル頻度ファイルを読み込み、結合する
freq_files = glob.glob(freq_dir + 'chr*.af.txt')
freq_data = pd.concat([pd.read_csv(file, sep='\t') for file in freq_files], ignore_index=True)

# VCFデータとアリル頻度データをIDをキーとしてマージする
merged_data = pd.merge(vcf_data, freq_data, on='ID', how='inner')

# 個体ごとのf2統計量の合計とカウントを初期化
sample_names = ['FM020_FM020', 'Iyai4b_Iyai4b', 'Jomon_Jomon', 'Todo5_Todo5']
f2_totals = {sample: 0.0 for sample in sample_names}
counts = {sample: 0 for sample in sample_names}

# マージしたデータフレームに対してf2統計量を計算
for _, row in merged_data.iterrows():
    ref = row['REF_x']
    alt = row['ALT_x']
    freq_ref = row['REF_y']
    freq_alts = row['ALT_y'].split(',')
    freq_afs = list(map(float, row['AF'].split(',')))

    for i, sample in enumerate(sample_names):
        genotype = row[f'SAMPLE_{i+1}']
        for freq_alt, freq in zip(freq_alts, freq_afs):
            f2 = calculate_f2(genotype, ref, alt, freq_ref, freq_alt, freq)
            if f2 is not None:
                f2_totals[sample] += f2
                counts[sample] += 1
                break  # 一致するアリルが見つかったら他のアリルのチェックをスキップ

# 各個体のf2統計量を計算して出力
for sample in sample_names:
    f2_statistic = f2_totals[sample] / counts[sample] if counts[sample] > 0 else None
    print(f"{sample}のf2統計量: {f2_statistic}, 使用したSNPの数: {counts[sample]}")
