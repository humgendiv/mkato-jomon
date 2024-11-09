import pandas as pd


# VCFファイルのパスを指定
vcf_file_path = '/home/mkato/hdd_data/1-merged_data/for_PRS/merged/m_jomons_for_PRS.vcf'
import pandas as pd

def count_valid_genotypes(vcf_file):
    # VCFファイルを開き、ヘッダー行の検出
    with open(vcf_file, 'r') as f:
        for line in f:
            if line.startswith('#CHROM'):
                header = line.strip().split('\t')
                break
    
    # データ部分をヘッダーを指定して読み込み
    vcf_data = pd.read_csv(vcf_file, sep='\t', comment='#', names=header)

    # カラム名を確認
    print("Columns in VCF file:", vcf_data.columns)

    # サンプルのカラムを特定（9列目以降がサンプルのデータ）
    samples = vcf_data.columns[9:]

    # 有効なデータ（./. 以外）のカウント
    valid_counts = {}
    for sample in samples:
        valid_counts[sample] = (vcf_data[sample] != './.').sum()

    return valid_counts

# 有効なデータ数を計算
valid_counts = count_valid_genotypes(vcf_file_path)

# 結果を表示
for sample, count in valid_counts.items():
    print(f'{sample}: {count} valid entries')
