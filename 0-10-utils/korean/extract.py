import os
import gzip
import re
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def load_positions(positions_file):
    with open(positions_file, 'r') as file:
        return set(line.strip() for line in file)

def process_af_file(file_path, positions):
    input_dir = "/home/mkato/hdd_data/data/Genomes/korean/af"
    output_dir = "/home/mkato/hdd_data/data/Genomes/korean/af_filtered"
    
    # 出力ファイル名の生成
    output_file = os.path.join(output_dir, os.path.basename(file_path))
    
    os.makedirs(output_dir, exist_ok=True)  # 出力ディレクトリが存在しない場合は作成
    
    with open(file_path, 'r', encoding='utf-8') as input_txt, open(output_file, 'w', encoding='utf-8') as output_txt:
        # ヘッダー行を書き込む
        header = input_txt.readline()
        output_txt.write(header)
        
        for line in input_txt:
            fields = line.strip().split('\t')
            if fields[0] in positions:
                output_txt.write(line)

def main():
    positions_file = "/home/mkato/hdd_data/data/bim/merged_positions.bim"
    positions = load_positions(positions_file)
    
    input_dir = "/home/mkato/hdd_data/data/Genomes/korean/af"
    af_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith('.af.txt')]
    
    # 並行処理の設定
    num_processes = min(22, len(af_files))
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        futures = [executor.submit(process_af_file, file, positions) for file in af_files]
        for future in futures:
            future.result()

if __name__ == '__main__':
    main()
