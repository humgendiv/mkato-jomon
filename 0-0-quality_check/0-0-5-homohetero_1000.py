import gzip

def count_genotypes_in_vcf(vcf_file_path):
    homozygous_variant_counts = {}
    heterozygous_counts = {}
    homozygous_reference_counts = {}
    header_line = None

    with gzip.open(vcf_file_path, 'rt') as file:
        for line in file:
            if line.startswith('##'):
                continue  # Skip metadata lines

            if line.startswith('#'):
                header_line = line.strip().split('\t')
                continue

            data = line.strip().split('\t')
            if not header_line or len(data) <= 9:  # Ensure there's genotype data
                continue

            for i in range(9, len(header_line)):  # Genotype data starts at the 10th column
                individual_id = header_line[i]
                genotype_info = data[i].split(':')[0]  # Extract genotype before the first colon

                # Initialize counts for the individual if not already done
                if individual_id not in homozygous_variant_counts:
                    homozygous_variant_counts[individual_id] = 0
                    heterozygous_counts[individual_id] = 0
                    homozygous_reference_counts[individual_id] = 0
                
                # Counting homozygous (1|1) and heterozygous (0|1 or 1|0) sites
                if genotype_info == '1|1':
                    homozygous_variant_counts[individual_id] += 1
                elif genotype_info in ['0|1', '1|0']:
                    heterozygous_counts[individual_id] += 1
                elif genotype_info == '0|0':
                    homozygous_reference_counts[individual_id] += 1


    return homozygous_variant_counts, heterozygous_counts, homozygous_reference_counts

# Replace 'your_vcf_file.vcf.gz' with the actual path of your VCF file
vcf_file_path = '/home/mkato/hdd_data/data/0-0-raw_vcf/ALL.chr1.integrated_phase1_v3.20101123.snps_indels_svs.genotypes.vcf.gz'
homozygous_variant_counts, heterozygous_counts, homozygous_reference_counts = count_genotypes_in_vcf(vcf_file_path)

# Example: Print counts for the first few individuals
for individual in list(homozygous_variant_counts.keys())[:100]:
    print(f"Individual {individual}: Homo_variant {homozygous_variant_counts[individual]}, Hetero {heterozygous_counts[individual]}, Homo_reference {homozygous_reference_counts[individual]}")
