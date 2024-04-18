import itertools
import gzip

def read_vcf(file_path):
    with gzip.open(file_path, 'rt') as file:
        for line in file:
            if not line.startswith('#'):
                yield line.strip().split('\t')

def calculate_f2(genotypes1, genotypes2):
    assert len(genotypes1) == len(genotypes2)
    
    diff_sum = 0
    site_count = 0
    
    for gt1, gt2 in zip(genotypes1, genotypes2):
        if './.' not in [gt1, gt2]:
            freq1 = sum(int(allele) for allele in gt1.split('/')) / 2
            freq2 = sum(int(allele) for allele in gt2.split('/')) / 2
            diff_sum += (freq1 - freq2) ** 2
            site_count += 1
    
    return diff_sum / site_count if site_count > 0 else 0

vcf_file = '/home/mkato/hdd_data/data/0-4-merge_and_convert/m_0-3-extract_plink.vcf.gz'
samples = ['FM020_FM020', 'Iyai4b_Iyai4b', 'Jomon_Jomon', 'Todo5_Todo5']

genotypes = {sample: [] for sample in samples}

for record in read_vcf(vcf_file):
    if '.' not in [record[9], record[10], record[11], record[12]]:
        for i, sample in enumerate(samples, start=9):
            genotypes[sample].append(record[i].split(':')[0])

for sample1, sample2 in itertools.combinations(samples, 2):
    f2 = calculate_f2(genotypes[sample1], genotypes[sample2])
    print(f'F2({sample1}, {sample2}) = {f2:.4f}')
