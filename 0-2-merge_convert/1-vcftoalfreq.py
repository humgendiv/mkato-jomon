import sys

def calculate_allele_frequency(genotypes, ref, alt):
    total_alleles = len(genotypes) * 2
    ref_count = sum(g.count('0') for g in genotypes if g != './.')
    alt_count = sum(g.count('1') for g in genotypes if g != './.')
    ref_freq = ref_count / total_alleles
    alt_freq = alt_count / total_alleles
    return ref_freq, alt_freq

def process_vcf(input_file, output_file):
    with open(input_file, 'r') as vcf_file, open(output_file, 'w') as out_file:
        for line in vcf_file:
            if line.startswith('#'):
                out_file.write(line)
                if line.startswith('#CHROM'):
                    out_file.write('##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">\n')
            else:
                fields = line.strip().split('\t')
                ref = fields[3]
                alt = fields[4]
                genotypes = fields[9:]
                ref_freq, alt_freq = calculate_allele_frequency(genotypes, ref, alt)
                info_field = f'AF={alt_freq:.4f}'
                out_file.write('\t'.join(fields[:7]) + f'\t{info_field}\t' + '\t'.join(fields[8:]) + '\n')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_vcf> <output_vcf>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    process_vcf(input_file, output_file)
