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

# 個体ごとのf2統計量の合計とカウントを初期化
f2_totals = {'FM020_FM020': 0.0, 'Iyai4b_Iyai4b': 0.0, 'Jomon_Jomon': 0.0, 'Todo5_Todo5': 0.0}
counts = {'FM020_FM020': 0, 'Iyai4b_Iyai4b': 0, 'Jomon_Jomon': 0, 'Todo5_Todo5': 0}

# 各染色体のアリル頻度ファイルを読み込む
freq_files = glob.glob(freq_dir + 'chr*.af.txt')

# VCFファイルを行ごとに処理する
with open(vcf_file, 'r') as vcf:
    for line in vcf:
        if line.startswith('#'):
            continue  # ヘッダー行をスキップ

        fields = line.strip().split('\t')
        chrom, pos, id_, ref, alt = fields[0:5]
        genotypes = fields[9:13]
        sample_names = ['FM020_FM020', 'Iyai4b_Iyai4b', 'Jomon_Jomon', 'Todo5_Todo5']

        # 対応するアリル頻度ファイルを探す
        freq_file = freq_dir + f'chr{chrom}.af.txt'
        if freq_file in freq_files:
            freq_data = pd.read_csv(freq_file, sep='\t')

            # IDをキーとして一致する行を探す
            freq_row = freq_data[freq_data['ID'] == id_]
            if freq_row.empty:
                continue  # 該当する行がない場合はスキップ

            freq_row = freq_row.iloc[0]
            freq_ref = freq_row['REF']
            freq_alts = freq_row['ALT'].split(',')
            freq_afs = list(map(float, freq_row['AF'].split(',')))

            # 各個体の遺伝子型についてf2統計量を計算
            for i, sample in enumerate(sample_names):
                genotype = genotypes[i]
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

