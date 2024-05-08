import os
import gzip
import re
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def process_vcf_file(file_path):
    input_dir = "/home/mkato/hdd_data/data/Genomes/korean/prepro"
    output_dir = "/home/mkato/hdd_data/data/Genomes/korean/af"
    
    # 出力ファイル名の生成
    chr_num = re.findall(r'chr(\d+)', os.path.basename(file_path))[0]
    output_file = os.path.join(output_dir, f"chr{chr_num}.af.txt")
    os.makedirs(output_dir, exist_ok=True)
    
    with open(file_path, 'r') as input_vcf, open(output_file, 'w') as output_txt:
        output_txt.write("ID\tREF\tALT\tAF\n")
        for line in input_vcf:
            if not line.startswith('#'):
                fields = line.strip().split('\t')
                info_fields = dict(item.split('=') for item in fields[7].split(';') if '=' in item)
                af = info_fields.get('AF', 'NA')
                output_txt.write(f"{fields[2]}\t{fields[3]}\t{fields[4]}\t{af}\n")

def main():
    input_dir = "/home/mkato/hdd_data/data/Genomes/korean/prepro"
    vcf_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith('.vcf')]
    
    # 並行処理の設定
    num_processes = min(22, len(vcf_files))
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(process_vcf_file, file) for file in vcf_files]
        for future in futures:
            future.result()

if __name__ == '__main__':
    main()
