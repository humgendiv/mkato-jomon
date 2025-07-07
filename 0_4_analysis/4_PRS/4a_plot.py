"""
PRSの計算結果をプロットする。
PRSは、IyaiとOtherJomonの値に対して、ModernJapaneseの値を引くことで現代人との差を可視化する。
traitは、平均値でsortし、平均値が高いものを上に表示する。
指標群を臓器・機能別にグループ分けして色分けし、解釈しやすくする。
2集団は色を分けてわかりやすく表示する。
入力ファイルは、/home/mkato/hdd_data/0_4_analysis/4_PRS/PRS_scores内に3ファイルあるのでそれぞれに対してプロットする。
出力は、/home/mkato/mkato-jomon/0_4_analysis/4_PRS/plot内に保存する。
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from matplotlib.colors import LinearSegmentedColormap

def get_trait_groups():
    """指標を主要な6グループに分類"""
    groups = {
        'Anthropometry': ['BMI', 'Height'],
        'Inflammation_Immune': ['WBC', 'Neutro', 'Lym', 'Mono', 'Eosino', 'Baso', 'CRP'],
        'Metabolism': ['TC', 'LDL-C', 'TG', 'HDL-C', 'BS', 'HbA1c', 'UA'],
        'Cardiovascular': ['SBP', 'DBP', 'MAP', 'PP', 'EF', 'FS', 'LVM', 'LVMI', 'LVDd', 'LVDs', 'IVS', 'PW', 'RWT', 'EA'],
        'Liver': ['GGT', 'AST', 'ALT', 'TBil', 'ALP', 'LDH', 'ZTT', 'Alb', 'AG'],
        'Kidney': ['eGFR', 'BUN', 'sCr', 'Na', 'K', 'Cl', 'Ca', 'P']
    }
    return groups

def get_group_colors():
    """主要6グループの色を定義"""
    colors = {
        'Anthropometry': '#696969',      # ディムグレー
        'Inflammation_Immune': '#4169E1', # ロイヤルブルー
        'Metabolism': '#8B4513',         # サドルブラウン
        'Cardiovascular': '#DC143C',     # クリムゾン
        'Liver': '#32CD32',              # ライムグリーン
        'Kidney': '#00CED1'              # ダークターコイズ
    }
    return colors

def assign_trait_colors(traits):
    """各指標にグループ色を割り当て"""
    groups = get_trait_groups()
    colors = get_group_colors()
    
    trait_colors = {}
    trait_groups = {}
    
    # 各指標をグループに割り当て
    for trait in traits:
        assigned = False
        for group_name, group_traits in groups.items():
            if trait in group_traits:
                trait_colors[trait] = colors[group_name]
                trait_groups[trait] = group_name
                assigned = True
                break
        
        if not assigned:
            trait_colors[trait] = '#CCCCCC'  # ライトグレー（その他）
            trait_groups[trait] = 'Other'
    
    return trait_colors, trait_groups

def create_legend_patches(trait_groups, trait_colors):
    """凡例用のパッチを作成（Otherを最後に移動）"""
    from matplotlib.patches import Patch
    
    # グループごとに整理
    group_info = {}
    for trait, group in trait_groups.items():
        if group not in group_info:
            group_info[group] = {
                'color': trait_colors[trait],
                'traits': []
            }
        group_info[group]['traits'].append(trait)
    
    # Otherを分離
    other_info = group_info.pop('Other', None)
    
    # 凡例パッチを作成（メイングループ先、Other後）
    legend_patches = []
    for group, info in group_info.items():
        patch = Patch(color=info['color'], label=f"{group} ({len(info['traits'])})")
        legend_patches.append(patch)
    
    # Otherを最後に追加
    if other_info:
        patch = Patch(color=other_info['color'], label=f"Other ({len(other_info['traits'])})")
        legend_patches.append(patch)
    
    return legend_patches

def load_prs_data(file_path):
    """PRSデータを読み込み"""
    df = pd.read_csv(file_path, sep='\t', index_col=0)
    return df

def calculate_differences(df):
    """現代人との差分を計算"""
    # ModernJapaneseとの差分を計算
    iyai_diff = df['Iyai'] - df['ModernJapanese']
    other_jomon_diff = df['OtherJomon'] - df['ModernJapanese']
    
    # 差分データフレームを作成
    diff_df = pd.DataFrame({
        'Iyai': iyai_diff,
        'OtherJomon': other_jomon_diff,
        'Mean': (iyai_diff + other_jomon_diff) / 2
    })
    
    return diff_df

def create_plot(diff_df, p_value, output_path):
    """プロットを作成"""
    # 平均値でソート（降順）
    sorted_df = diff_df.sort_values('Mean', ascending=False)
    
    # 指標の色とグループを取得
    trait_colors, trait_groups = assign_trait_colors(sorted_df.index)
    
    # プロット設定
    fig, ax = plt.subplots(figsize=(14, max(10, len(sorted_df) * 0.5)))
    
    # Y軸の位置
    y_pos = np.arange(len(sorted_df))
    
    # 各指標の色を取得
    colors_iyai = [trait_colors[trait] for trait in sorted_df.index]
    colors_other = [trait_colors[trait] for trait in sorted_df.index]
    
    # プロット作成（色分け + パターン、順序修正）
    width = 0.35
    bars1 = ax.barh(y_pos + width/2, sorted_df['Iyai'], width, 
                   label='Iyai', color=colors_iyai, alpha=0.8, 
                   edgecolor='black', linewidth=0.8)
    bars2 = ax.barh(y_pos - width/2, sorted_df['OtherJomon'], width, 
                   label='OtherJomon', color=colors_other, alpha=0.8, 
                   edgecolor='black', linewidth=0.8, hatch='///')
    
    # 軸設定
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_df.index, fontsize=10)
    ax.set_xlabel('PRS Difference from Modern Japanese', fontsize=12)
    ax.set_title(f'PRS Differences by Organ/Function Groups (p < {p_value})', fontsize=14)
    
    # ゼロライン
    ax.axvline(x=0, color='black', linestyle='--', alpha=0.7, linewidth=2)
    
    # グリッド
    ax.grid(True, alpha=0.3, axis='x')
    
    # 集団の凡例（枠内右上）
    from matplotlib.patches import Rectangle
    population_patches = [
        Rectangle((0, 0), 1, 1, facecolor='white', edgecolor='black', linewidth=1.5, label='Iyai'),
        Rectangle((0, 0), 1, 1, facecolor='white', edgecolor='black', linewidth=1.5, hatch='///', label='OtherJomon')
    ]
    population_legend = ax.legend(handles=population_patches, loc='upper right', 
                                bbox_to_anchor=(0.98, 0.98), fontsize=12)
    
    # グループの凡例を追加（集団凡例のすぐ下）
    legend_patches = create_legend_patches(trait_groups, trait_colors)
    group_legend = ax.legend(handles=legend_patches, loc='upper right', 
                           bbox_to_anchor=(0.98, 0.95), fontsize=12)
    
    # 両方の凡例を表示
    ax.add_artist(population_legend)
    
    # レイアウト調整
    plt.tight_layout()
    
    # 保存
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"プロット保存: {output_path}")

def main():
    # パス設定
    input_dir = "/home/mkato/hdd_data/0_4_analysis/4_PRS/PRS_scores"
    output_dir = "/home/mkato/mkato-jomon/0_4_analysis/4_PRS/plot"
    
    # 出力ディレクトリ作成
    os.makedirs(output_dir, exist_ok=True)
    
    # 入力ファイル一覧取得
    input_files = glob.glob(os.path.join(input_dir, "PRS_scores_p*.tsv"))
    
    print(f"処理対象ファイル数: {len(input_files)}")
    
    # matplotlib日本語フォント設定
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
    # 各ファイルについて処理
    for input_file in input_files:
        filename = os.path.basename(input_file)
        print(f"処理中: {filename}")
        
        try:
            # p値を抽出
            p_value = filename.replace('PRS_scores_p', '').replace('.tsv', '')
            
            # データ読み込み
            df = load_prs_data(input_file)
            
            # 差分計算
            diff_df = calculate_differences(df)
            
            # プロット作成
            output_file = os.path.join(output_dir, f"PRS_differences_grouped_p{p_value}.png")
            create_plot(diff_df, p_value, output_file)
            
        except Exception as e:
            print(f"エラー: {filename} - {str(e)}")
            continue
    
    print("全ての処理が完了しました。")

if __name__ == "__main__":
    main()