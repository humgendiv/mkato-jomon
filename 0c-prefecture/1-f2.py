import gzip
import itertools
import pandas as pd

def read_vcf(file_path, samples):
    with gzip.open(file_path, 'rt') as file:
        header = []
        for line in file:
            if line.startswith('#CHROM'):
                header = line.strip().split('\t')[9:]  # サンプル名を取得
            if not line.startswith('#'):
                fields = line.strip().split('\t')
                chrom, pos = fields[0], fields[1]
                ref, alt = fields[3], fields[4]
                genotypes = [gt.split(':')[0] for gt in fields[9:]]
                sample_genotypes = [genotypes[header.index(sample)] if sample in header else './.' for sample in samples]
                if './.' not in sample_genotypes:  # すべてのサンプルに有効なジェノタイプがあるか
                    yield chrom, pos, ref, alt, sample_genotypes

def read_freq_file(file_path):
    with open(file_path, 'r') as file:
        next(file)  # ヘッダー行をスキップ
        for line in file:
            chrom, pos_id, ref, alt, alt_freq, obs_ct = line.strip().split()
            pos = pos_id.split(':')[1]
            yield chrom, pos, ref, alt, float(alt_freq)

def calculate_f2(freq1, freq2):
    return (freq1 - freq2) ** 2

vcf_file = '/home/mkato/hdd_data/2-1-prefectural_conparison/Pruned/jomon.vcf.gz'
freq_file_prefix = '/home/mkato/hdd_data/2-1-prefectural_conparison/prefectural_afreq_data/vM_QC_PC_bi.Rsq03'
freq_file_suffix = '.rand50.afreq'
prefectures = [f'ken{i}' for i in range(1, 48)]
samples = ['0_FM020', '0_FM027-1_DS_PG0301_005', '0_FM027-2_DS_PG0301_005', '0_I1', '0_Jomon', '0_DO', '0_T5']

vcf_data = {}
for chrom, pos, ref, alt, sample_genotypes in read_vcf(vcf_file, samples):
    vcf_data[(chrom, pos)] = (ref, alt, sample_genotypes)

f2_results = []

for prefecture in prefectures:
    freq_file = f'{freq_file_prefix}.{prefecture}{freq_file_suffix}'
    freq_data = {}
    for chrom, pos, ref, alt, alt_freq in read_freq_file(freq_file):
        if (chrom, pos) in vcf_data:
            vcf_ref, vcf_alt, genotypes = vcf_data[(chrom, pos)]
            if (ref, alt) == (vcf_ref, vcf_alt):
                freq_data[(chrom, pos)] = alt_freq
            elif (ref, alt) == (vcf_alt, vcf_ref):
                freq_data[(chrom, pos)] = 1 - alt_freq

    for i, sample in enumerate(samples):
        jomon_freqs = []
        prefecture_freqs = []
        for (chrom, pos), alt_freq in freq_data.items():
            genotype = vcf_data[(chrom, pos)][2][i]
            if genotype != './.':
                jomon_freq = sum(int(allele) for allele in genotype.split('/')) / 2
                jomon_freqs.append(jomon_freq)
                prefecture_freqs.append(alt_freq)
        
        if len(jomon_freqs) > 0:  # 有効なジェノタイプがあるか確認
            f2 = sum(calculate_f2(jf, pf) for jf, pf in zip(jomon_freqs, prefecture_freqs)) / len(jomon_freqs)
            print(f"length of jomon_freqs: {len(jomon_freqs)}, length of prefecture_freqs: {len(prefecture_freqs)}")
            print(f'F2({sample}, {prefecture}) = {f2:.4f}')
            f2_results.append({'Sample': sample, 'Prefecture': prefecture, 'F2': f2})

f2_df = pd.DataFrame(f2_results)
f2_pivot = f2_df.pivot(index='Sample', columns='Prefecture', values='F2')
print(f2_pivot)

f2_pivot.to_csv('Pruned.f2_pivot.csv')
