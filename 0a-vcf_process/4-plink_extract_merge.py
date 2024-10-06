import os
import subprocess
import yaml

# 設定ファイルを読み込む関数
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

# SNPをextractする関数
def extract_snps_for_sample(sample_name, extract_file, sample_dir, output_dir):
    processed_dir = os.path.join(sample_dir, "processed")
    extracted_dir = os.path.join(sample_dir, "extracted")

    # extract_fileのファイル名（拡張子除く）を抽出して動的に命名に使用
    extract_base_name = os.path.splitext(os.path.basename(extract_file))[0]

    if os.path.isdir(processed_dir):
        os.makedirs(extracted_dir, exist_ok=True)

        # processedフォルダ内の.bedファイルを探索してSNPを抽出
        for bed_file in os.listdir(processed_dir):
            if bed_file.endswith('.bed'):
                base_name = os.path.splitext(bed_file)[0]
                input_bfile = os.path.join(processed_dir, base_name)
                output_bfile = os.path.join(extracted_dir, f"{base_name}_extracted_{extract_base_name}")

                # plinkコマンドでSNPを抽出
                plink_cmd = [
                    "plink",
                    "--bfile", input_bfile,
                    "--extract", extract_file,
                    "--make-bed",
                    "--out", output_bfile
                ]
                subprocess.run(plink_cmd, check=True)
                print(f"Extracted SNPs for {sample_name} from {bed_file}")

# 複数のパートファイルをマージする関数
def merge_sample_parts(sample_name, sample_dir, output_dir):
    extracted_dir = os.path.join(sample_dir, "extracted")
    merged_output = os.path.join(output_dir, f"{sample_name}_merged")

    # .bimファイルを基にマージリストを生成
    merge_list_file = os.path.join(extracted_dir, "merge_list.txt")
    with open(merge_list_file, 'w') as f:
        for file in os.listdir(extracted_dir):
            if file.endswith('.bim'):
                base_name = os.path.splitext(file)[0]
                f.write(f"{os.path.join(extracted_dir, base_name)}\n")

    # PLINKでマージ処理
    plink_merge_cmd = [
        "plink",
        "--merge-list", merge_list_file,
        "--make-bed",
        "--out", merged_output
    ]
    try:
        subprocess.run(plink_merge_cmd, check=True)
        print(f"Merged part files for {sample_name} into {merged_output}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to merge parts for {sample_name}. Error: {e}")

# メイン処理
def main(config_file):
    config = load_config(config_file)
    parent_dir = config['parent_dir']
    output_dir = config['output_dir']
    extract_file = config['extract_file']
    samples = config['samples']

    # `samples` が空欄または空リストの場合、parent_dirの全ディレクトリを対象にする
    if not samples:
        samples = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]

    # 各サンプルについてSNPの抽出とマージを順次実行
    for sample_name in samples:
        sample_dir = os.path.join(parent_dir, sample_name)
        print(f"Processing sample: {sample_name}")

        # 1. extract処理
        extract_snps_for_sample(sample_name, extract_file, sample_dir, output_dir)

        # 2. パートファイルのマージ
        merge_sample_parts(sample_name, sample_dir, output_dir)

    print("All samples have been processed.")

# スクリプトの実行
if __name__ == "__main__":
    config_file = "4-plink_extract_merge.yaml"
    main(config_file)
