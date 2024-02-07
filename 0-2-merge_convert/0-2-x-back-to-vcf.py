import gzip

def count_genotypes_in_vcf_gz(file_path):
    genotype_counts = {}
    sample_names = []

    with gzip.open(file_path, 'rt') as file:
        for line in file:
            if line.startswith('##'):
                continue
            if line.startswith('#CHROM'):
                header_parts = line.strip().split('\t')
                sample_names = header_parts[9:]
                for name in sample_names:
                    genotype_counts[name] = {'heterozygous': 0, 'homozygous': 0, 'missing_value': 0, '0/0':0}
                continue

            columns = line.strip().split('\t')
            genotypes = columns[9:]
            continue_flag = 0
            for i, genotype in enumerate(genotypes):
                if i == 0:
                    continue
                if genotype == './.':
                    continue_flag = 1
                    break
            for i, genotype in enumerate(genotypes):
                if continue_flag == 1:
                    break
                if genotype == './.': #in ['.', './.', '.|.','.|.']:
                    genotype_counts[sample_names[i]]['missing_value'] += 1
                elif genotype == '1/0' or genotype == '0/1':
                    genotype_counts[sample_names[i]]['heterozygous'] += 1         
                elif genotype == '1/1':
                    genotype_counts[sample_names[i]]['homozygous'] += 1
                elif genotype == '0/0':
                    genotype_counts[sample_names[i]]['0/0'] += 1


    return genotype_counts


print(count_genotypes_in_vcf_gz("/home/mkato/hdd_data/data/0-3-1-back_to_vcf/plink.vcf.gz"))