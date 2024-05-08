import os
import gzip
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def process_vcf_file(file_path):
    input_dir = "/home/mkato/hdd_data/data/Genomes/korean"
    output_dir = "/home/mkato/hdd_data/data/Genomes/korean/id"
    
    # IDのCHR:POS形式での付与
    output_file = os.path.join(output_dir, f"{os.path.splitext(file_path)[0]}.updated.vcf.gz")
    with open(os.path.join(input_dir, file_path), 'r') as input_vcf, gzip.open(output_file, 'wt') as output_vcf:
        for line in input_vcf:
            if not line.startswith('#'):
                fields = line.strip().split('\t')
                chrom = fields[0].replace('chr', '')  # CHROMからchrを除去
                fields[2] = f"{chrom}:{fields[1]}"
                output_vcf.write('\t'.join(fields) + '\n')
            else:
                output_vcf.write(line)
    
    # merged_position.bimに基づく抽出
    bim_file = "/home/mkato/hdd_data/data/bim/merged_positions.bim"
    with open(bim_file, 'r') as bim:
        for line in bim:
            chr_pos = line.strip()
            chr, pos = chr_pos.split(':')
            output_file = os.path.join(output_dir, f"{chr_pos}.vcf.gz")
            with gzip.open(output_file, 'wt') as output_vcf:
                with gzip.open(os.path.join(output_dir, f"chr{chr}.recal.vcf.updated.vcf.gz"), 'rt') as input_vcf:
                    for vcf_line in input_vcf:
                        if not vcf_line.startswith('#'):
                            fields = vcf_line.strip().split('\t')
                            if fields[2] == chr_pos:
                                output_vcf.write(vcf_line)
                        else:
                            output_vcf.write(vcf_line)

def main():
    input_dir = "/home/mkato/hdd_data/data/Genomes/korean"
    vcf_files = [file for file in os.listdir(input_dir) if file.endswith('.vcf.gz')]
    
    # 並行処理の設定
    num_processes = min(22, len(vcf_files))
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(process_vcf_file, file) for file in vcf_files]
        for future in futures:
            future.result()

if __name__ == '__main__':
    main()
