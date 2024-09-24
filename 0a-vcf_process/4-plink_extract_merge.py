import os
import subprocess
import yaml

# 設定ファイルを読み込む関数
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config

# SNPをextractする関数
def extract_snps(parent_dir, extract_file):
    # parent_dir内のサンプルフォルダを探索
    for folder in os.listdir(parent_dir):
        folder_path = os.path.join(parent_dir, folder)
        processed_dir = os.path.join(folder_path, "processed")
        extracted_dir = os.path.join(folder_path, "extracted")

        if os.path.isdir(processed_dir):
            os.makedirs(extracted_dir, exist_ok=True)  # extractedディレクトリを作成

            # processedフォルダ内の.bedファイルを探索してSNPを抽出
            for bed_file in os.listdir(processed_dir):
                if bed_file.endswith('.bed'):
                    base_name = os.path.splitext(bed_file)[0]
                    input_bfile = os.path.join(processed_dir, base_name)
                    output_bfile = os.path.join(extracted_dir, f"{base_name}_extracted_1240K")
                    
                    # plinkコマンドでSNPを抽出
                    plink_cmd = [
                        "plink",
                        "--bfile", input_bfile,
                        "--extract", extract_file,
                        "--make-bed",
                        "--out", output_bfile
                    ]
                    subprocess.run(plink_cmd, check=True)
                    print(f"Extracted SNPs for {folder} from {bed_file}")

# 複数のplinkファイルをマージする関数
def merge_plink_files(parent_dir, output_dir, final_output_name):
    os.makedirs(output_dir, exist_ok=True)

    # ファイル名リストを生成
    output_txt = os.path.join(output_dir, "output.txt")
    with open(output_txt, 'w') as f:
        for folder in os.listdir(parent_dir):
            extracted_dir = os.path.join(parent_dir, folder, "extracted")
            if os.path.isdir(extracted_dir):
                for file in os.listdir(extracted_dir):
                    if file.endswith('.bim'):
                        base_name = os.path.splitext(file)[0]
                        f.write(f"{os.path.join(extracted_dir, base_name)}\n")
    print("merge_list created")

    # plinkでマージ処理
    final_output_prefix = os.path.join(output_dir, final_output_name)
    plink_merge_cmd = [
        "plink",
        "--merge-list", output_txt,
        "--out", final_output_prefix
    ]
    subprocess.run(plink_merge_cmd, check=True)
    print("Merge trial done")

    # missnpファイルがある場合
    missnp_file = f"{final_output_prefix}.missnp"
    if os.path.exists(missnp_file):
        print("missnp is found, excluding and retrying merge")
        tmp_txt = os.path.join(output_dir, "output.tmp.txt")
        with open(output_txt, 'r') as f_in, open(tmp_txt, 'w') as f_out:
            for line in f_in:
                line = line.strip()
                tmp_output = f"{line}.tmp"
                exclude_cmd = [
                    "plink",
                    "--make-bed",
                    "--exclude", missnp_file,
                    "--bfile", line,
                    "--chr", "1-22",
                    "--out", tmp_output
                ]
                subprocess.run(exclude_cmd, check=True)
                f_out.write(f"{tmp_output}\n")
        
        # 再度マージ
        final_merge_cmd = [
            "plink",
            "--merge-list", tmp_txt,
            "--out", final_output_prefix
        ]
        subprocess.run(final_merge_cmd, check=True)

        # クリーンアップ
        os.remove(output_txt)
        os.remove(tmp_txt)
        os.remove(missnp_file)
        print("Temporary files cleaned up")

# メイン処理
def main(config_file):
    # 設定ファイルの読み込み
    config = load_config(config_file)
    parent_dir = config['parent_dir']
    extract_file = config['extract_file']
    output_dir = config['output_dir']
    final_output_name = config['final_output_name']

    # SNPの抽出
    extract_snps(parent_dir, extract_file)

    # プリンクファイルのマージ
    merge_plink_files(parent_dir, output_dir, final_output_name)

# スクリプトの実行
if __name__ == "__main__":
    config_file = "4-plink_extract_merge.yaml"
    main(config_file)


