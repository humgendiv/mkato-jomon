"""
PRSの計算結果をボルケーノプロットで可視化する。
IyaiとOtherJomonの値に対して、ModernJapaneseの値を引くことで現代人との差を可視化する。
Iyai（時間的に前の集団）とOtherJomon（時間的に後の集団）の比較をボルケーノプロットで表示。
4a_plot.pyの色分けとグループ分けを完全に準拠。
入力ファイルは、/home/mkato/hdd_data/0_4_analysis/4_PRS/PRS_scores内に3ファイルあるのでそれぞれに対してプロットする。
出力は、/home/mkato/mkato-jomon/0_4_analysis/4_PRS/plot内に保存する。
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from scipy import stats
import matplotlib.patches as mpatches

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
        patch = mpatches.Patch(color=info['color'], label=f"{group} ({len(info['traits'])})")
        legend_patches.append(patch)
    
    # Otherを最後に追加
    if other_info:
        patch = mpatches.Patch(color=other_info['color'], label=f"Other ({len(other_info['traits'])})")
        legend_patches.append(patch)
    
    return legend_patches

def load_prs_data(file_path):
    """PRSデータを読み込み"""
    df = pd.read_csv(file_path, sep='\t', index_col=0)
    return df

def calculate_volcano_data(df):
    """ボルケーノプロット用のデータを計算"""
    # ModernJapaneseとの差分を計算（4a_plot.pyと同じ計算法）
    iyai_diff = df['Iyai'] - df['ModernJapanese']
    other_jomon_diff = df['OtherJomon'] - df['ModernJapanese']
    
    # Fold Change計算：OtherJomon（後の集団）/ Iyai（前の集団）の比
    # 小さな値での除算を避けるため、小さな定数を追加
    epsilon = 0.1
    
    # 差分の絶対値が小さい場合は1に近い値を返す
    fold_changes = []
    for i, trait in enumerate(df.index):
        iyai_val = iyai_diff.iloc[i]
        other_val = other_jomon_diff.iloc[i]
        
        # 両方の値が小さい場合
        if abs(iyai_val) < epsilon and abs(other_val) < epsilon:
            fc = 1.0
        # Iyaiがゼロに近い場合
        elif abs(iyai_val) < epsilon:
            fc = np.sign(other_val) * abs(other_val) / epsilon
        else:
            fc = other_val / iyai_val
        
        fold_changes.append(fc)
    
    # Log2 Fold Changeを計算
    log2_fc = np.log2(np.abs(fold_changes)) * np.sign(fold_changes)
    
    # Log2 FCの極端な値をクリップ（可視化のため）
    log2_fc = np.clip(log2_fc, -8, 8)
    
    # Y軸の指標を計算
    # 方法1: 単純な差の大きさ（統計的検定なし）
    diff_magnitude = np.abs(other_jomon_diff - iyai_diff)
    
    # 方法2: 効果量（Cohen's d的な指標）
    # 平均差を標準的なスケールで正規化
    mean_abs_diff = np.mean(np.abs(np.concatenate([iyai_diff.values, other_jomon_diff.values])))
    if mean_abs_diff > 0:
        effect_size = diff_magnitude / mean_abs_diff
    else:
        effect_size = diff_magnitude
    
    # 方法3: 差分の比率（どれだけ異なるか）
    min_abs = np.minimum(np.abs(iyai_diff), np.abs(other_jomon_diff)) + epsilon
    relative_diff = diff_magnitude / min_abs
    
    # デフォルトでは効果量を使用（より解釈しやすい）
    y_metric = effect_size
    
    # Y軸の値を上限でクリップ（可読性向上のため）
    y_max = 3.5
    y_metric_clipped = np.clip(y_metric, 0, y_max)
    
    # データフレームを作成
    volcano_df = pd.DataFrame({
        'log2FC': log2_fc,
        'effect_size': y_metric_clipped,
        'effect_size_original': y_metric,  # クリップ前の値も保存
        'iyai_diff': iyai_diff,
        'other_jomon_diff': other_jomon_diff,
        'diff_magnitude': diff_magnitude,
        'relative_diff': relative_diff
    }, index=df.index)
    
    return volcano_df

def create_volcano_plot(volcano_df, p_value, output_path):
    """ボルケーノプロットを作成"""
    # 指標の色とグループを取得
    trait_colors, trait_groups = assign_trait_colors(volcano_df.index)
    
    # プロット設定
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # クリップされた指標を追跡
    clipped_traits = []
    
    # 効果量と変化の閾値を設定
    effect_threshold = 1.0  # 中程度の効果
    fc_threshold = 1.0  # 2倍の変化
    
    # 各指標をプロット
    for trait in volcano_df.index:
        color = trait_colors[trait]
        x = volcano_df.loc[trait, 'log2FC']
        y = volcano_df.loc[trait, 'effect_size']
        y_original = volcano_df.loc[trait, 'effect_size_original']
        
        # サイズは差の大きさに基づく（スケール調整）
        size = np.sqrt(volcano_df.loc[trait, 'diff_magnitude']) * 15
        size = np.clip(size, 30, 300)  # サイズの範囲を制限
        
        # クリップされた場合は特別なマーカーを使用
        if y_original > y:
            ax.scatter(x, y, c=color, s=size, alpha=0.8, edgecolors='black', linewidth=0.8, marker='^')
            clipped_traits.append(trait)
        else:
            ax.scatter(x, y, c=color, s=size, alpha=0.8, edgecolors='black', linewidth=0.8)
        
        # 重要な指標にラベルを追加
        # 条件：効果量が大きい、または変化が大きい
        if (y > effect_threshold and abs(x) > fc_threshold) or y > 1.5 or abs(x) > 2:
            # クリップされた場合は元の値も表示
            label_text = trait
            if y_original > y:
                label_text = f"{trait}*"
            
            # ラベルの位置を調整（重なりを避ける）
            offset_x = 8 if x > 0 else -8
            offset_y = 8
            ha = 'left' if x > 0 else 'right'
            
            ax.annotate(label_text, (x, y), fontsize=9, alpha=0.9,
                       xytext=(offset_x, offset_y), textcoords='offset points',
                       ha=ha, va='bottom',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', 
                               alpha=0.8, edgecolor=color, linewidth=1))
    
    # 閾値線（効果量の参考値）
    ax.axhline(y=0.5, color='gray', linestyle='--', alpha=0.4, linewidth=1)
    ax.axhline(y=1.0, color='gray', linestyle=':', alpha=0.4, linewidth=1.5)
    ax.axhline(y=2.0, color='gray', linestyle='-.', alpha=0.4, linewidth=1)
    
    # Fold changeの閾値線
    ax.axvline(x=-1, color='gray', linestyle='--', alpha=0.4, linewidth=1)
    ax.axvline(x=1, color='gray', linestyle='--', alpha=0.4, linewidth=1)
    ax.axvline(x=0, color='black', linestyle='-', alpha=0.3, linewidth=1)
    
    # 四分割の背景色（オプション）
    ax.axhspan(0, effect_threshold, alpha=0.02, color='gray')
    ax.axvspan(-fc_threshold, fc_threshold, alpha=0.02, color='gray')
    
    # Y軸の上限を設定（3.5に変更）
    ax.set_ylim(0, 3.5)
    
    # X軸の範囲も調整
    x_max = max(abs(volcano_df['log2FC'].min()), abs(volcano_df['log2FC'].max())) + 0.5
    ax.set_xlim(-x_max, x_max)
    
    # 軸ラベル（タイトルは削除、p値情報は注釈に含める）
    ax.set_xlabel('Log2 Fold Change (OtherJomon / Iyai)\n← Iyai higher | OtherJomon higher →', fontsize=13, fontweight='bold')
    ax.set_ylabel('Effect Size (Normalized Difference)', fontsize=13, fontweight='bold')
    
    # グリッド（より見やすく）
    ax.grid(True, alpha=0.25, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)  # グリッドを背面に
    
    # 凡例を作成
    legend_patches = create_legend_patches(trait_groups, trait_colors)
    legend1 = ax.legend(handles=legend_patches, loc='upper left', fontsize=10, 
                       framealpha=0.95, edgecolor='black', fancybox=True)
    
    # 注釈を追加（右下に移動、p値情報を含める）
    note_text = f'p < {p_value}\n'
    note_text += 'Point size ∝ magnitude of difference\n'
    note_text += 'Y-axis = |Δ(OtherJomon) - Δ(Iyai)| / mean|Δ|\n'
    note_text += 'Gray lines: Effect size 0.5, 1.0, 2.0\n'
    note_text += 'Vertical lines: 2-fold change (FC=2)'
    if clipped_traits:
        note_text += f'\n▲ = values clipped (n={len(clipped_traits)})'
    
    ax.text(0.98, 0.02, note_text, transform=ax.transAxes,
            fontsize=9, verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9, edgecolor='gray'))
    
    # 軸のスタイル調整
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    
    # レイアウト調整
    plt.tight_layout()
    
    # 保存
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"ボルケーノプロット保存: {output_path}")
    if clipped_traits:
        print(f"  クリップされた指標: {', '.join(clipped_traits)}")

def create_supplementary_plot(volcano_df, p_value, output_path):
    """補足的な散布図を作成（Iyai vs OtherJomon の直接比較）"""
    # 指標の色とグループを取得
    trait_colors, trait_groups = assign_trait_colors(volcano_df.index)
    
    # プロット設定
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 各指標をプロット
    for trait in volcano_df.index:
        color = trait_colors[trait]
        x = volcano_df.loc[trait, 'iyai_diff']
        y = volcano_df.loc[trait, 'other_jomon_diff']
        
        ax.scatter(x, y, c=color, s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        # 全ての指標にラベルを追加
        ax.annotate(trait, (x, y), fontsize=8, alpha=0.8,
                   xytext=(5, 5), textcoords='offset points')
    
    # 対角線（y=x）
    lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),
        np.max([ax.get_xlim(), ax.get_ylim()]),
    ]
    ax.plot(lims, lims, 'k--', alpha=0.5, zorder=0)
    
    # ゼロライン
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
    
    # 軸ラベルとタイトル
    ax.set_xlabel('Iyai PRS (difference from Modern Japanese)', fontsize=12)
    ax.set_ylabel('OtherJomon PRS (difference from Modern Japanese)', fontsize=12)
    ax.set_title(f'Direct Comparison of PRS Differences (p < {p_value})', fontsize=14)
    
    # グリッド
    ax.grid(True, alpha=0.3)
    
    # 凡例を作成
    legend_patches = create_legend_patches(trait_groups, trait_colors)
    ax.legend(handles=legend_patches, loc='upper left', fontsize=10, framealpha=0.9)
    
    # アスペクト比を等しく
    ax.set_aspect('equal', adjustable='box')
    
    # レイアウト調整
    plt.tight_layout()
    
    # 保存
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"補足プロット保存: {output_path}")


def create_group_summary_plot(volcano_df, p_value, output_path):
    """形質群ごとの傾向を示すサマリープロット"""
    # 指標の色とグループを取得
    trait_colors, trait_groups = assign_trait_colors(volcano_df.index)
    groups = get_trait_groups()
    colors = get_group_colors()
    
    # グループごとにデータを集計
    group_stats = {}
    for group_name in list(groups.keys()) + ['Other']:
        # このグループに属する指標を抽出
        group_traits = [t for t, g in trait_groups.items() if g == group_name]
        
        if group_traits:
            group_data = volcano_df.loc[group_traits]
            
            # 各種統計量を計算
            stats = {
                'n': len(group_traits),
                'mean_log2FC': group_data['log2FC'].mean(),
                'std_log2FC': group_data['log2FC'].std(),
                'mean_effect': group_data['effect_size'].mean(),
                'std_effect': group_data['effect_size'].std(),
                'median_log2FC': group_data['log2FC'].median(),
                'median_effect': group_data['effect_size'].median(),
                # 方向性の一貫性（何％が同じ方向か）
                'consistency': (group_data['log2FC'] > 0).sum() / len(group_traits)
            }
            
            # 色を取得
            if group_name != 'Other':
                stats['color'] = colors[group_name]
            else:
                stats['color'] = '#CCCCCC'
                
            group_stats[group_name] = stats
    
    # プロット作成（2つのサブプロット）
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # サブプロット1: グループ別ボルケーノプロット（平均値と標準誤差）
    for group_name, stats in group_stats.items():
        if stats['n'] > 0:
            # エラーバー付きでプロット
            ax1.errorbar(stats['mean_log2FC'], stats['mean_effect'],
                        xerr=stats['std_log2FC']/np.sqrt(stats['n']),
                        yerr=stats['std_effect']/np.sqrt(stats['n']),
                        fmt='o', markersize=15, color=stats['color'],
                        alpha=0.8, capsize=5, capthick=2, linewidth=2,
                        label=f"{group_name} (n={stats['n']})")
            
            # グループ名を点の近くに表示
            ax1.annotate(group_name, 
                        (stats['mean_log2FC'], stats['mean_effect']),
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=10, fontweight='bold', alpha=0.9)
    
    # 参照線
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    ax1.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    ax1.axhline(y=0.5, color='gray', linestyle='--', alpha=0.4)
    ax1.axhline(y=1.0, color='gray', linestyle=':', alpha=0.4)
    
    ax1.set_xlabel('Mean Log2 Fold Change (OtherJomon / Iyai)', fontsize=12)
    ax1.set_ylabel('Mean Effect Size', fontsize=12)
    ax1.set_title(f'Group-level Summary (p < {p_value})', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10, framealpha=0.9)
    
    # サブプロット2: 方向性の一貫性を示すバープロット
    group_names = []
    consistencies = []
    bar_colors = []
    
    # Otherを最後に配置
    ordered_groups = [g for g in group_stats.keys() if g != 'Other']
    if 'Other' in group_stats:
        ordered_groups.append('Other')
    
    for group_name in ordered_groups:
        stats = group_stats[group_name]
        group_names.append(f"{group_name}\n(n={stats['n']})")
        # OtherJomon方向の割合を表示
        consistencies.append(stats['consistency'] * 100)
        bar_colors.append(stats['color'])
    
    # バープロット
    bars = ax2.bar(range(len(group_names)), consistencies, color=bar_colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # 50%ライン
    ax2.axhline(y=50, color='red', linestyle='--', alpha=0.7, linewidth=2)
    
    ax2.set_xticks(range(len(group_names)))
    ax2.set_xticklabels(group_names, fontsize=11)
    ax2.set_ylabel('Traits with OtherJomon > Iyai (%)', fontsize=12)
    ax2.set_title('Directional Consistency by Group', fontsize=14)
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # パーセンテージを各バーの上に表示
    for i, (bar, pct) in enumerate(zip(bars, consistencies)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{pct:.0f}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # 全体のレイアウト調整
    plt.tight_layout()
    
    # 保存
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"グループサマリープロット保存: {output_path}")
    
    # 統計情報も出力
    print("\nグループ別統計:")
    for group_name in ordered_groups:
        stats = group_stats[group_name]
        print(f"  {group_name}: n={stats['n']}, "
              f"mean_log2FC={stats['mean_log2FC']:.2f}, "
              f"mean_effect={stats['mean_effect']:.2f}, "
              f"OtherJomon>Iyai={stats['consistency']*100:.1f}%")
    """補足的な散布図を作成（Iyai vs OtherJomon の直接比較）"""
    # 指標の色とグループを取得
    trait_colors, trait_groups = assign_trait_colors(volcano_df.index)
    
    # プロット設定
    fig, ax = plt.subplots(figsize=(10, 10))
    
    # 各指標をプロット
    for trait in volcano_df.index:
        color = trait_colors[trait]
        x = volcano_df.loc[trait, 'iyai_diff']
        y = volcano_df.loc[trait, 'other_jomon_diff']
        
        ax.scatter(x, y, c=color, s=100, alpha=0.7, edgecolors='black', linewidth=0.5)
        
        # 全ての指標にラベルを追加
        ax.annotate(trait, (x, y), fontsize=8, alpha=0.8,
                   xytext=(5, 5), textcoords='offset points')
    
    # 対角線（y=x）
    lims = [
        np.min([ax.get_xlim(), ax.get_ylim()]),
        np.max([ax.get_xlim(), ax.get_ylim()]),
    ]
    ax.plot(lims, lims, 'k--', alpha=0.5, zorder=0)
    
    # ゼロライン
    ax.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='gray', linestyle='-', alpha=0.3)
    
    # 軸ラベルとタイトル
    ax.set_xlabel('Iyai PRS (difference from Modern Japanese)', fontsize=12)
    ax.set_ylabel('OtherJomon PRS (difference from Modern Japanese)', fontsize=12)
    ax.set_title(f'Direct Comparison of PRS Differences (p < {p_value})', fontsize=14)
    
    # グリッド
    ax.grid(True, alpha=0.3)
    
    # 凡例を作成
    legend_patches = create_legend_patches(trait_groups, trait_colors)
    ax.legend(handles=legend_patches, loc='upper left', fontsize=10, framealpha=0.9)
    
    # アスペクト比を等しく
    ax.set_aspect('equal', adjustable='box')
    
    # レイアウト調整
    plt.tight_layout()
    
    # 保存
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"補足プロット保存: {output_path}")

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
            
            # ボルケーノプロット用データ計算
            volcano_df = calculate_volcano_data(df)
            
            # ボルケーノプロット作成
            volcano_output = os.path.join(output_dir, f"PRS_volcano_plot_p{p_value}.png")
            create_volcano_plot(volcano_df, p_value, volcano_output)
            
            # グループサマリープロット作成
            summary_output = os.path.join(output_dir, f"PRS_group_summary_p{p_value}.png")
            create_group_summary_plot(volcano_df, p_value, summary_output)
            
            # 補足プロット作成
            scatter_output = os.path.join(output_dir, f"PRS_scatter_comparison_p{p_value}.png")
            create_supplementary_plot(volcano_df, p_value, scatter_output)
            
        except Exception as e:
            print(f"エラー: {filename} - {str(e)}")
            continue
    
    print("全ての処理が完了しました。")

if __name__ == "__main__":
    main()