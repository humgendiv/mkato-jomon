import os
import gzip
import csv

def load_af_data(af_dir):
    af_data = {}
    total_af_snps = 0
    for i in range(1, 23):
        file_path = os.path.join(af_dir, f"chr{i}.af.txt")
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter='\t')
            for row in reader:
                snp_id, ref = row['ID'], row['REF']
                alts = row['ALT'].split(',')
                afs = [float(af) for af in row['AF'].split(',')]
                af_data[snp_id] = {'REF': ref, 'ALT': alts, 'AF': afs}
                total_af_snps += 1
    return af_data, total_af_snps

def calculate_f2(freq1, freq2):
    return (freq1 - freq2) ** 2

def calculate_f2_values(vcf_file, af_data):
    f2_values = {sample: 0 for sample in ["FM020_FM020", "Iyai4b_Iyai4b", "Jomon_Jomon", "Todo5_Todo5"]}
    num_snps = {sample: 0 for sample in ["FM020_FM020", "Iyai4b_Iyai4b", "Jomon_Jomon", "Todo5_Todo5"]}
    total_snps = 0
    total_jomon_snps = 0
    
    with open(vcf_file, 'r') as file:
        for line in file:
            if not line.startswith('#'):
                total_jomon_snps += 1
                fields = line.strip().split('\t')
                chrom, pos, snp_id, ref, alt = fields[:5]
                genotypes = fields[9:]
                
                if snp_id in af_data:
                    af_ref = af_data[snp_id]['REF']
                    af_alts = af_data[snp_id]['ALT']
                    afs = af_data[snp_id]['AF']
                    
                    if ref == af_ref and alt in af_alts:
                        # ALT and REF match
                        alt_index = af_alts.index(alt)
                        af = afs[alt_index]
                        for i, sample in enumerate(["FM020_FM020", "Iyai4b_Iyai4b", "Jomon_Jomon", "Todo5_Todo5"]):
                            genotype = genotypes[i]
                            if genotype == '0/0':
                                f2_values[sample] += calculate_f2(0, af)
                            elif genotype in ['0/1', '1/0']:
                                f2_values[sample] += calculate_f2(0.5, af)
                            elif genotype == '1/1':
                                f2_values[sample] += calculate_f2(1, af)
                            num_snps[sample] += 1
                        total_snps += 1
                    elif alt == af_ref and ref in af_alts:
                        # ALT and REF are inverted
                        ref_index = af_alts.index(ref)
                        inverted_af = afs[ref_index]
                        for i, sample in enumerate(["FM020_FM020", "Iyai4b_Iyai4b", "Jomon_Jomon", "Todo5_Todo5"]):
                            genotype = genotypes[i]
                            if genotype == '0/0':
                                f2_values[sample] += calculate_f2(1, inverted_af)
                            elif genotype in ['0/1', '1/0']:
                                f2_values[sample] += calculate_f2(0.5, inverted_af)
                            elif genotype == '1/1':
                                f2_values[sample] += calculate_f2(0, inverted_af)
                            num_snps[sample] += 1
                        total_snps += 1
                    # REFはref, af_refで一致しているが、ALTはaf_altは問題ないが、af_altが”.”になっている場合。
                    elif alt == af_ref and af_alts[0] == '.':
                    else:
                        print(f"alt: {alt}, ref: {ref}, af_alts: {af_alts}, af_ref: {af_ref}")
    
    # Calculate average F2 values
    for sample in f2_values:
        if num_snps[sample] > 0:
            f2_values[sample] /= num_snps[sample]
    
    return f2_values, total_snps, total_jomon_snps

def main():
    af_dir = "/home/mkato/hdd_data/data/Genomes/korean/af"
    vcf_file = "/home/mkato/hdd_data/data/Genomes/korean/jomon_korean_comm/merged/m_jomon_fullkorean_complete.vcf"
    
    af_data, total_af_snps = load_af_data(af_dir)
    f2_values, total_snps, total_jomon_snps = calculate_f2_values(vcf_file, af_data)
    
    print("F2 values:")
    for sample, f2 in f2_values.items():
        print(f"{sample}: {f2}")
    
    print(f"\nTotal SNPs in the allele frequency data: {total_af_snps}")
    print(f"Total SNPs in the Jomon data: {total_jomon_snps}")
    print(f"Total SNPs included in the calculation: {total_snps}")

if __name__ == '__main__':
    main()
