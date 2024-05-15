import gzip
import itertools
import pandas as pd

def read_vcf(file_path):
    with gzip.open(file_path, 'rt') as file:
        for line in file:
            if not line.startswith('#'):
                yield line.strip().split('\t')

def read_freq_file(file_path):
    with open(file_path, 'r') as file:
        next(file)  # ヘッダー行をスキップ
        for line in file:
            chrom, pos_id, ref, alt, alt_freq, obs_ct = line.strip().split()
            pos = pos_id.split(':')[1]
            yield chrom, pos, ref, alt, float(alt_freq)

def calculate_f2(freq1, freq2):
    return (freq1 - freq2) ** 2

vcf_file = '/home/mkato/hdd_data/data/0-4-merge_and_convert/Pruned.m_0-3-extract_plink.vcf.gz'
freq_file_prefix = '/home/mkato/hdd_data/data/Prefecture/prefectural_afreq_data/vM_QC_PC_bi.Rsq03'
freq_file_suffix = '.rand50.afreq'
prefectures = [f'ken{i}' for i in range(1, 48)]
samples = ['FM020_FM020', 'Iyai4b_Iyai4b', 'Jomon_Jomon', 'Todo5_Todo5']

vcf_data = {}
for record in read_vcf(vcf_file):
    chrom, pos = record[0], record[1]
    ref, alt = record[3], record[4]
    genotypes = [gt.split(':')[0] for gt in record[9:]]
    if './.' not in genotypes:
        vcf_data[(chrom, pos)] = (ref, alt, genotypes)

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
            jomon_freq = sum(int(allele) for allele in genotype.split('/')) / 2
            jomon_freqs.append(jomon_freq)
            prefecture_freqs.append(alt_freq)
        
        f2 = sum(calculate_f2(jf, pf) for jf, pf in zip(jomon_freqs, prefecture_freqs)) / len(jomon_freqs)
        print(f"length of jomon_freqs: {len(jomon_freqs)}, length of prefecture_freqs: {len(prefecture_freqs)}")
        print(f'F2({sample}, {prefecture}) = {f2:.4f}')
        f2_results.append({'Sample': sample, 'Prefecture': prefecture, 'F2': f2})

f2_df = pd.DataFrame(f2_results)
f2_pivot = f2_df.pivot(index='Sample', columns='Prefecture', values='F2')
print(f2_pivot)

f2_pivot.to_csv('Pruned.f2_pivot.csv')
