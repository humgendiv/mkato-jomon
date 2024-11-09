import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# ディレクトリのパス設定
roh_files_path = "/home/mkato/hdd_data/2-5-HBD/ROH/*.hom"
output_figure_path = "/home/mkato/hdd_data/2-5-HBD/ROH/ROH_summary_plot.png"  # 保存先のファイルパス

# 除外したいサンプルのリスト
exclude_samples = ["FM027-2", "FM027-1"]

# すべての .hom ファイルを読み込み
all_hom_files = glob.glob(roh_files_path)
df_list = []

for file in all_hom_files:
    df = pd.read_csv(file, delim_whitespace=True)
    
    # ファイル名からサンプル名を抽出（パート番号を無視して同じサンプル名で統合するために）
    sample_name = os.path.basename(file).split('_')[0]  # "_"で分割し、サンプル名部分を取得
    
    # 除外リストにあるサンプルはスキップ
    if sample_name in exclude_samples:
        print(f"Excluding {sample_name}")
        continue
    
    df['sample'] = sample_name  # 統一されたサンプル名を追加
    df_list.append(df)

# すべてのデータを1つのDataFrameに結合
combined_df = pd.concat(df_list, ignore_index=True)

# ROH長をMb単位に変換
combined_df['ROH_length_Mb'] = combined_df['KB'] / 1000

# カテゴリを設定（例: 0.5Mb, 1Mb, 2Mb, 4Mb, 8Mb, 16Mbなど）
categories = [0.5, 1, 2, 4, 8, 16, 32, 64, 100]

# 各カテゴリごとのROHの長さの総和を計算
results = {}

# サンプル名ごとに集計
for sample in combined_df['sample'].unique():
    sample_data = combined_df[combined_df['sample'] == sample]
    counts = []
    for i in range(len(categories) - 1):
        count = sample_data[(sample_data['ROH_length_Mb'] > categories[i]) &
                            (sample_data['ROH_length_Mb'] <= categories[i+1])]['ROH_length_Mb'].sum()
        counts.append(count)
    results[sample] = counts

# グラフのプロット
fig, ax = plt.subplots()

for sample, counts in results.items():
    ax.plot(categories[:-1], counts, label=sample)

ax.set_xscale('log')
ax.set_xlabel('Runs of homozygosity (Mb)')
ax.set_ylabel('Total length of ROH per individual (Mb)')
ax.legend()

# 画像として保存
plt.savefig(output_figure_path, dpi=300)  # 解像度300dpiで保存
print(f"Figure saved to {output_figure_path}")

plt.show()
