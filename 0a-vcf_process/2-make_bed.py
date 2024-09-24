import os
import subprocess
import yaml
from concurrent.futures import ProcessPoolExecutor

# 設定ファイルを読み込む関数
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

# PLINK形式に変換する関数
def vcf_to_plink(input_vcf, output_prefix, chrom_range):
    bed_prefix = f"{output_prefix}_part_{chrom_range.replace(',', '_').replace('-', '_')}"
    
    # PLINK --make-bedを使って、VCFを変換する
    plink_cmd = [
        "plink", 
        "--vcf", input_vcf,
        "--make-bed", 
        "--out", bed_prefix,
        #"--memory", "4000",  # メモリ制限の例
        "--chr", chrom_range,  # 分割対象の染色体番号の範囲を指定
        "--allow-extra-chr",  # 23番染色体以降を無視しない
        "--const-fid",  # FIDを一定にする
    ]
    
    print(f"Running PLINK: {' '.join(plink_cmd)}")
    subprocess.run(plink_cmd, check=True)
    print(f"Finished PLINK for {bed_prefix}")

# メイン処理
def main(config_file):
    # 設定ファイルの読み込み
    config = load_config(config_file)
    parent_path = config['parent_path']
    target_folders = config['target_folders']

    # 染色体番号で5つの範囲に分割
    chromosome_ranges = [
        "1-4",      # 第1グループ: 1-4番染色体
        "5-8",      # 第2グループ: 5-8番染色体
        "9-12",     # 第3グループ: 9-12番染色体
        "13-16",    # 第4グループ: 13-16番染色体
        "17-22"  # 第5グループ: 17-22番染色体、X、Y、MT
    ]

    # 並列実行用のプール
    with ProcessPoolExecutor() as executor:
        futures = []
        
        for folder in target_folders:
            processed_dir = os.path.join(parent_path, folder, "processed")
            
            # 対象フォルダ内の.vcf.gzファイルを探す
            vcf_files = [f for f in os.listdir(processed_dir) if f.endswith('.vcf.gz')]
            
            for vcf_file in vcf_files:
                input_vcf = os.path.join(processed_dir, vcf_file)
                output_prefix = os.path.join(processed_dir, vcf_file.replace(".vcf.gz", ""))
                
                # 染色体範囲ごとに並列でPLINK形式に変換
                for chrom_range in chromosome_ranges:
                    future = executor.submit(vcf_to_plink, input_vcf, output_prefix, chrom_range)
                    futures.append(future)
        
        # 全てのタスクが完了するのを待つ
        for future in futures:
            future.result()

# スクリプトの実行
if __name__ == "__main__":
    config_file = "2-make_bed.yaml"  # 設定ファイルのパス
    main(config_file)

