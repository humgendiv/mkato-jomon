import gzip

# VCF.gzファイルを読み込み、ジェノタイプをカウントする関数
def count_genotypes(vcf_gz_file):
    count_1_1 = 0
    count_0_1_or_1_0 = 0
    count_0_0 = 0
    count_missing =0

    with gzip.open(vcf_gz_file, 'rt') as file:  # 'rt'はテキストモードで読み込むことを指定
        for line in file:
            if line.startswith('#'):
                # コメント行は無視する
                continue
            else:
                # ジェノタイプ情報を取得
                parts = line.split('\t')
                genotype_info = parts[9].split(':')[0]

                # ジェノタイプをカウント
                if genotype_info == '1/1':
                    count_1_1 += 1
                elif genotype_info in ['0/1', '1/0']:
                    count_0_1_or_1_0 += 1
                elif genotype_info == '0/0':
                    count_0_0 += 1
                elif genotype_info == './.':
                    count_missing += 1

    return count_1_1, count_0_1_or_1_0, count_0_0, count_missing

# VCF.gzファイルパス
sample_name = 'I4'
#vcf_gz_file = f'/home/mkato/hdd_data/data/0-0-raw_vcf/{sample_name}.vcf.gz'
vcf_gz_file = f'/home/mkato/hdd_data/data/0-1-filtered_vcf/{sample_name}_filtered2.vcf.gz'
# カウントを実行
count_1_1, count_0_1_or_1_0,count_0_0, count_missing = count_genotypes(vcf_gz_file)
print(sample_name+'filtered')
print(f"1/1 Genotypes: {count_1_1}")
print(f"0/1 or 1/0 Genotypes: {count_0_1_or_1_0}")
print(f"0/0 Genotypes: {count_0_0}")
print(f"missing value: {count_missing}")
