import re
import gzip
import os
import yaml
from concurrent.futures import ProcessPoolExecutor

# 設定ファイルを読み込む関数
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

# VCFファイルの処理を行う関数
def process_vcf(input_file, output_file, options, filter_depth):
    with gzip.open(input_file, 'rt') as infile, gzip.open(output_file, 'wt') as outfile:
        for line in infile:
            if line.startswith('#'):
                if line.startswith('##contig') or line.startswith('#CHROM'):
                    if options['remove_chr_prefix']:
                        line = re.sub(r'chr(\d+)', r'\1', line)
                outfile.write(line)
            else:
                fields = line.strip().split('\t')
                chrom = fields[0]
                pos = fields[1]
                alt = fields[4]
                info = fields[7]
                format_info = fields[8]
                sample_info = fields[9]
                
                # CHROMフィールドの'chr'プレフィックス削除
                if options['remove_chr_prefix']:
                    fields[0] = re.sub(r'^chr', '', chrom)
                
                # ALTフィールドの'<NON_REF>'削除・置換
                if options['remove_non_ref']:
                    fields[4] = re.sub(r',<NON_REF>', '', alt)
                    fields[4] = re.sub(r'^<NON_REF>$', '.', fields[4])
                
                # FORMATフィールドのDPとGTのインデックス取得
                format_fields = format_info.split(':')
                dp_index = format_fields.index('DP') if 'DP' in format_fields else -1
                gt_index = format_fields.index('GT') if 'GT' in format_fields else -1
                
                # フィルタリング条件：DPが指定値以上かつGTが'./.'でない
                if dp_index != -1 and gt_index != -1:
                    sample_fields = sample_info.split(':')
                    depth = int(sample_fields[dp_index])
                    genotype = sample_fields[gt_index]
                    if depth >= filter_depth and genotype != './.':
                        # IDフィールドをCHROM:POS形式に変更
                        if options['assign_id']:
                            fields[2] = f"{fields[0]}:{pos}"
                        
                        # END情報の展開
                        if options['expand_end']:
                            end_match = re.search(r'END=(\d+)', info)
                            if end_match:
                                end_pos = int(end_match.group(1))
                                for new_pos in range(int(pos) + 1, end_pos + 1):
                                    new_fields = fields.copy()
                                    new_fields[1] = str(new_pos)
                                    new_fields[2] = f"{fields[0]}:{new_pos}"
                                    new_fields[3] = '.'
                                    outfile.write('\t'.join(new_fields) + '\n')
                            else:
                                outfile.write('\t'.join(fields) + '\n')
                        else:
                            outfile.write('\t'.join(fields) + '\n')

# メイン処理
def main(config_file):
    config = load_config(config_file)
    parent_path = config['parent_path']
    target_folders = config['target_folders']
    options = config['options']
    filter_depth = config['filter_depth']
    output_suffix = config['output_suffix']

    # ProcessPoolExecutorで並列処理
    with ProcessPoolExecutor() as executor:
        futures = []
        for folder in target_folders:
            input_folder = os.path.join(parent_path, folder)
            output_folder = os.path.join(input_folder, output_suffix)
            os.makedirs(output_folder, exist_ok=True)

            # VCFファイルのリストを取得（既に処理されたファイルは除外）
            vcf_files = [f for f in os.listdir(input_folder) if f.endswith('.vcf.gz') and not f.endswith(f'.{output_suffix}.vcf.gz')]

            for filename in vcf_files:
                input_file = os.path.join(input_folder, filename)
                output_file = os.path.join(output_folder, filename)
                future = executor.submit(process_vcf, input_file, output_file, options, filter_depth)
                futures.append(future)
        
        # 全タスクの完了を待機
        for future in futures:
            future.result()

# スクリプトの実行
if __name__ == '__main__':
    config_file = '1-process_vcf.yaml'  # 設定ファイルのパス
    main(config_file)

