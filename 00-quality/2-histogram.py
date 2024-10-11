def extract_dp_data(file_path):
    dp_data = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('DP'):
                # DPのデータを抽出して格納 (例: DP 0 10 0 0.000000 13223784 0.493462)
                parts = line.split()
                try:
                    bin_value = int(parts[2])  # 3列目のbin (depth)
                    num_sites = int(parts[5])  # 6列目のnumber of sites
                    dp_data.append((bin_value, num_sites))
                except ValueError:
                    print(f"DPデータの解析に失敗しました: {line}")
    return dp_data




import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt
import numpy as np

def plot_dp_histogram(dp_data, output_file, sample_name):
    # デプスと対応する頻度を分離
    depths = [x[0] for x in dp_data]  # bin (depth)
    frequencies = [x[1] for x in dp_data]  # number of sites

    plt.figure(figsize=(10, 6))
    plt.bar(depths, frequencies, color='blue', alpha=0.7)
    plt.title(f'DP Histogram for {sample_name}')  # タイトルにサンプル名を追加
    plt.xlabel('Depth (DP)')
    plt.ylabel('Number of Sites')
    plt.xlim(0, 100)  # 0から100までの範囲で固定
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()

def calculate_and_save_dp_average(dp_data, output_file):
    total_weighted_depth = 0  # 重み付きデプスの合計
    total_sites = 0  # 全サイト数

    for bin_value, num_sites in dp_data:
        total_weighted_depth += bin_value * num_sites  # binにnumber of sitesを掛ける
        total_sites += num_sites  # number of sitesを合計

    if total_sites > 0:
        average_depth = total_weighted_depth / total_sites  # 加重平均を計算
    else:
        average_depth = 0

    # 結果をテキストファイルに保存
    with open(output_file, 'w') as f:
        f.write(f"Average Depth (DP): {average_depth:.2f}\n")
    
    print(f"デプスの平均を保存しました: {output_file}")


import os

def process_sample_folders(directory):
    # サンプルフォルダの中にあるstats.txtを探す
    for sample_folder in os.listdir(directory):
        sample_path = os.path.join(directory, sample_folder)
        if os.path.isdir(sample_path):
            stats_file = os.path.join(sample_path, 'stats.txt')
            if os.path.exists(stats_file):
                dp_data = extract_dp_data(stats_file)
                
                if dp_data:
                    output_file = os.path.join(sample_path, 'dp_histogram.png')
                    plot_dp_histogram(dp_data, output_file, sample_folder)  # サンプル名をタイトルに追加
                    print(f"ヒストグラムを生成しました: {output_file}")
                else:
                    print(f"DPデータが見つかりません: {stats_file}")
            else:
                print(f"stats.txtが見つかりません: {sample_path}")

import os

def process_sample_folders_for_average(directory):
    # サンプルフォルダの中にあるstats.txtを探す
    for sample_folder in os.listdir(directory):
        sample_path = os.path.join(directory, sample_folder)
        if os.path.isdir(sample_path):
            stats_file = os.path.join(sample_path, 'stats.txt')
            if os.path.exists(stats_file):
                dp_data = extract_dp_data(stats_file)
                
                if dp_data:
                    output_file = os.path.join(sample_path, 'dp_average.txt')
                    calculate_and_save_dp_average(dp_data, output_file)  # 平均を計算して保存
                else:
                    print(f"DPデータが見つかりません: {stats_file}")
            else:
                print(f"stats.txtが見つかりません: {sample_path}")

# 実行
process_sample_folders_for_average('/home/mkato/hdd_data/0-genome_data/')


# 実行
process_sample_folders('/home/mkato/hdd_data/0-genome_data/')
