import os
import subprocess
import yaml

# 設定ファイルを読み込む関数
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

# データセットとサンプルデータをマージする関数
def merge_datasets(dataset_bfile, sample_bfile, output_bfile):
    # plink --bmerge コマンドを使用してデータセットとサンプルデータをマージ
    merge_cmd = [
        "plink",
        "--bfile", dataset_bfile,
        "--bmerge", sample_bfile + ".bed", sample_bfile + ".bim", sample_bfile + ".fam",
        "--make-bed",
        "--out", output_bfile
    ]

    try:
        subprocess.run(merge_cmd, check=True)
        print(f"Successfully merged {dataset_bfile} and {sample_bfile} into {output_bfile}")
    except subprocess.CalledProcessError:
        print("Initial merge failed. Attempting to exclude multiallelic variants.")
        handle_multiallelic_exclusion(dataset_bfile, sample_bfile, output_bfile)

# multi-allelic variants を除外して再マージする関数
def handle_multiallelic_exclusion(dataset_bfile, sample_bfile, output_bfile):
    missnp_file = f"{output_bfile}-merge.missnp"
    if not os.path.exists(missnp_file):
        print(f"Error: missnp file {missnp_file} not found.")
        return

    print(f"Excluding multiallelic SNPs listed in {missnp_file} and retrying merge.")
    
    # dataset_bfile から missnp SNPs を除外して、新しいセットを作成
    tmp_dataset_bfile = dataset_bfile + "_cleaned"
    exclude_cmd_dataset = [
        "plink",
        "--bfile", dataset_bfile,
        "--exclude", missnp_file,
        "--make-bed",
        "--out", tmp_dataset_bfile
    ]
    subprocess.run(exclude_cmd_dataset, check=True)

    # sample_bfile から missnp SNPs を除外して、新しいセットを作成
    tmp_sample_bfile = sample_bfile + "_cleaned"
    exclude_cmd_sample = [
        "plink",
        "--bfile", sample_bfile,
        "--exclude", missnp_file,
        "--make-bed",
        "--out", tmp_sample_bfile
    ]
    subprocess.run(exclude_cmd_sample, check=True)

    # 除外したデータセットで再度マージ
    retry_merge_cmd = [
        "plink",
        "--bfile", tmp_dataset_bfile,
        "--bmerge", tmp_sample_bfile + ".bed", tmp_sample_bfile + ".bim", tmp_sample_bfile + ".fam",
        "--make-bed",
        "--out", output_bfile,
        "--allow-no-sex"
    ]
    try:
        subprocess.run(retry_merge_cmd, check=True)
        print("Final merge completed successfully after excluding multiallelic SNPs.")
    except subprocess.CalledProcessError:
        print("Final merge attempt failed. Please check the data for further issues.")

    # クリーンアップ
    cleanup_files([tmp_dataset_bfile, tmp_sample_bfile])

# 不要な中間ファイルを削除する関数
def cleanup_files(files_to_remove):
    for file_base in files_to_remove:
        for ext in ['.bed', '.bim', '.fam']:
            file = file_base + ext
            if os.path.exists(file):
                os.remove(file)
        print(f"Removed temporary files for {file_base}")

# メイン処理
def main(config_file):
    # 設定ファイルの読み込み
    config = load_config(config_file)
    dataset_bfile = config['dataset_bfile']
    sample_bfile = config['sample_bfile']
    output_bfile = config['output_bfile']

    # データセットとサンプルデータをマージ
    merge_datasets(dataset_bfile, sample_bfile, output_bfile)

# スクリプトの実行
if __name__ == "__main__":
    config_file = "5-dataset_merge.yaml"
    main(config_file)

