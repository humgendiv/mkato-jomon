"""
PRSの計算結果を「差の大きさ」に焦点を当てて可視化する。
高低の意味が形質によって異なることを考慮し、絶対的な差の大きさと
その統計的意味を強調する新しいアプローチ。
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from scipy import stats
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import seaborn as sns

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
        'Anthropometry': '#696969',
        'Inflammation_Immune': '#4169E1',
        'Metabolism': '#8B4513',
        'Cardiovascular': '#DC143C',
        'Liver': '#32CD32',
        'Kidney': '#00CED1'
    }
    return colors

def assign_trait_colors(traits):
    """各指標にグループ色を割り当て"""
    groups = get_trait_groups()
    colors = get_group_colors()
    
    trait_colors = {}
    trait_groups = {}
    
    for trait in traits:
        assigned = False
        for group_name, group_traits in groups.items():
            if trait in group_traits:
                trait_colors[trait] = colors[group_name]
                trait_groups[trait] = group_name
                assigned = True
                break
        
        if not assigned:
            trait_colors[trait] = '#CCCCCC'
            trait_groups[trait] = 'Other'
    
    return trait_colors, trait_groups

def load_prs_data(file_path):
    """PRSデータを読み込み"""
    df = pd.read_csv(file_path, sep='\t', index_col=0)
    return df

def calculate_difference_metrics(df):
    """差の大きさを中心とした指標を計算"""
    # ModernJapaneseとの差分を計算
    iyai_diff = df['Iyai'] - df['ModernJapanese']
    other_jomon_diff = df['OtherJomon'] - df['ModernJapanese']
    
    # 1. 絶対的な差の大きさ
    absolute_difference = np.abs(other_jomon_diff - iyai_diff)
    
    # 2. 差の方向（OtherJomonがIyaiより高いか）
    direction = np.sign(other_jomon_diff - iyai_diff)
    
    # 3. 相対的な差の大きさ（全体の変動に対する比率）
    all_values = np.concatenate([iyai_diff.values, other_jomon_diff.values])
    global_std = np.std(all_values)
    if global_std > 0:
        standardized_difference = absolute_difference / global_std
    else:
        standardized_difference = absolute_difference
    
    # 4. 各形質の変動係数（どれだけ安定しているか）
    trait_variability = []
    for trait in df.index:
        values = [iyai_diff[trait], other_jomon_diff[trait]]
        cv = np.std(values) / (np.mean(np.abs(values)) + 0.01)
        trait_variability.append(cv)
    
    # 5. Modernとの距離（両集団がModernからどれだけ離れているか）
    modern_distance = (np.abs(iyai_diff) + np.abs(other_jomon_diff)) / 2
    
    # データフレームを作成
    metrics_df = pd.DataFrame({
        'absolute_diff': absolute_difference,
        'standardized_diff': standardized_difference,
        'direction': direction,
        'iyai_diff': iyai_diff,
        'other_jomon_diff': other_jomon_diff,
        'variability': trait_variability,
        'modern_distance': modern_distance
    }, index=df.index)
    
    return metrics_df

def create_difference_volcano(metrics_df, p_value, output_path):
    """差の大きさに焦点を当てたボルケーノプロット"""
    trait_colors, trait_groups = assign_trait_colors(metrics_df.index)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # プロットの準備
    x = metrics_df['absolute_diff']  # 絶対的な差の大きさ
    y = metrics_df['modern_distance']  # Modernからの距離
    
    # 方向で形を変える
    for trait in metrics_df.index:
        xi = metrics_df.loc[trait, 'absolute_diff']
        yi = metrics_df.loc[trait, 'modern_distance']
        color = trait_colors[trait]
        direction = metrics_df.loc[trait, 'direction']
        
        # サイズは標準化された差に基づく
        size = metrics_df.loc[trait, 'standardized_diff'] * 50
        size = np.clip(size, 50, 500)
        
        # 方向によってマーカーを変える
        if direction > 0:  # OtherJomon > Iyai
            marker = '^'
            label_prefix = '↑'
        elif direction < 0:  # Iyai > OtherJomon
            marker = 'v'
            label_prefix = '↓'
        else:
            marker = 'o'
            label_prefix = '='
        
        ax.scatter(xi, yi, c=color, s=size, alpha=0.7, 
                  edgecolors='black', linewidth=1, marker=marker)
        
        # 重要な形質にラベル
        if xi > np.percentile(x, 75) or yi > np.percentile(y, 75):
            ax.annotate(f'{label_prefix}{trait}', (xi, yi), 
                       fontsize=9, alpha=0.9,
                       xytext=(8, 8), textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.3', 
                               facecolor='white', alpha=0.8, 
                               edgecolor=color, linewidth=1))
    
    # 軸ラベル
    ax.set_xlabel('Absolute Difference Between Iyai and OtherJomon\n(Magnitude of population divergence)', 
                 fontsize=13, fontweight='bold')
    ax.set_ylabel('Average Distance from Modern Japanese\n(Degree of ancestral trait)', 
                 fontsize=13, fontweight='bold')
    ax.set_title(f'Population Difference Analysis (p < {p_value})', fontsize=15, fontweight='bold')
    
    # 参照線
    ax.axvline(x=np.median(x), color='gray', linestyle='--', alpha=0.4, linewidth=1)
    ax.axhline(y=np.median(y), color='gray', linestyle='--', alpha=0.4, linewidth=1)
    
    # グリッド
    ax.grid(True, alpha=0.25, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)
    
    # 凡例（グループ）
    from matplotlib.patches import Patch
    group_patches = []
    for group, color in get_group_colors().items():
        n_traits = sum(1 for g in trait_groups.values() if g == group)
        if n_traits > 0:
            patch = Patch(color=color, label=f'{group} ({n_traits})')
            group_patches.append(patch)
    
    # Other グループ
    n_other = sum(1 for g in trait_groups.values() if g == 'Other')
    if n_other > 0:
        patch = Patch(color='#CCCCCC', label=f'Other ({n_other})')
        group_patches.append(patch)
    
    legend1 = ax.legend(handles=group_patches, loc='upper right', 
                       fontsize=10, framealpha=0.95, title='Trait Groups')
    
    # 方向の凡例
    direction_patches = [
        plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='gray', 
                  markersize=10, label='OtherJomon > Iyai'),
        plt.Line2D([0], [0], marker='v', color='w', markerfacecolor='gray', 
                  markersize=10, label='Iyai > OtherJomon')
    ]
    legend2 = ax.legend(handles=direction_patches, loc='upper left', 
                       fontsize=10, framealpha=0.95, title='Direction')
    ax.add_artist(legend1)
    
    # 注釈
    note_text = 'Point size ∝ standardized difference\n'
    note_text += 'X-axis: How different are the populations?\n'
    note_text += 'Y-axis: How far from modern baseline?'
    
    ax.text(0.02, 0.02, note_text, transform=ax.transAxes,
            fontsize=9, verticalalignment='bottom',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                     alpha=0.9, edgecolor='gray'))
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"差分ボルケーノプロット保存: {output_path}")

def create_difference_heatmap(metrics_df, p_value, output_path):
    """形質群ごとの差の大きさをヒートマップで可視化"""
    trait_colors, trait_groups = assign_trait_colors(metrics_df.index)
    
    # データを並び替え（グループごと、差の大きさ順）
    sorted_traits = []
    group_boundaries = []
    current_pos = 0
    
    for group in list(get_trait_groups().keys()) + ['Other']:
        group_traits = [t for t, g in trait_groups.items() if g == group]
        if group_traits:
            # グループ内で差の大きさでソート
            group_df = metrics_df.loc[group_traits].sort_values('absolute_diff', ascending=False)
            sorted_traits.extend(group_df.index.tolist())
            group_boundaries.append((current_pos, current_pos + len(group_traits), group))
            current_pos += len(group_traits)
    
    # ヒートマップ用データ準備
    heatmap_data = []
    for trait in sorted_traits:
        row = [
            metrics_df.loc[trait, 'iyai_diff'],
            metrics_df.loc[trait, 'other_jomon_diff'],
            metrics_df.loc[trait, 'absolute_diff'] * metrics_df.loc[trait, 'direction']
        ]
        heatmap_data.append(row)
    
    heatmap_df = pd.DataFrame(heatmap_data, 
                              index=sorted_traits,
                              columns=['Iyai vs Modern', 'OtherJomon vs Modern', 'Population Difference'])
    
    # プロット
    fig, axes = plt.subplots(1, 2, figsize=(16, max(10, len(sorted_traits) * 0.25)), 
                             gridspec_kw={'width_ratios': [3, 1]})
    
    # ヒートマップ
    sns.heatmap(heatmap_df, ax=axes[0], cmap='RdBu_r', center=0, 
                cbar_kws={'label': 'PRS Difference', 'shrink': 0.8},
                linewidths=0.5, linecolor='gray', annot=False)
    
    axes[0].set_ylabel('Traits', fontsize=12)
    axes[0].set_xlabel('Comparison', fontsize=12)
    axes[0].set_title(f'PRS Difference Heatmap (p < {p_value})', fontsize=14, fontweight='bold')
    
    # グループの境界線と色を追加
    for start, end, group in group_boundaries:
        if group != 'Other':
            color = get_group_colors()[group]
        else:
            color = '#CCCCCC'
        axes[0].axhspan(start, end, xmin=-0.01, xmax=0, 
                        color=color, alpha=0.8, clip_on=False, in_layout=False)
    
    # 差の大きさのバープロット
    abs_diff = metrics_df.loc[sorted_traits, 'absolute_diff'].values
    colors_list = [trait_colors[t] for t in sorted_traits]
    
    bars = axes[1].barh(range(len(sorted_traits)), abs_diff, 
                        color=colors_list, alpha=0.7, edgecolor='black', linewidth=0.5)
    
    axes[1].set_ylim(axes[0].get_ylim())
    axes[1].set_xlabel('Absolute Difference', fontsize=12)
    axes[1].set_title('Magnitude', fontsize=12)
    axes[1].set_yticks([])
    axes[1].invert_yaxis()
    
    # 中央値ライン
    median_diff = np.median(abs_diff)
    axes[1].axvline(x=median_diff, color='red', linestyle='--', alpha=0.5, label=f'Median: {median_diff:.2f}')
    axes[1].legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"差分ヒートマップ保存: {output_path}")

def create_group_variability_plot(metrics_df, p_value, output_path):
    """グループごとの変動性と差の分布を可視化"""
    trait_colors, trait_groups = assign_trait_colors(metrics_df.index)
    
    # グループごとにデータを集計
    group_data = {}
    for group in list(get_trait_groups().keys()) + ['Other']:
        group_traits = [t for t, g in trait_groups.items() if g == group]
        if group_traits:
            group_metrics = metrics_df.loc[group_traits]
            group_data[group] = {
                'traits': group_traits,
                'abs_diff': group_metrics['absolute_diff'].values,
                'std_diff': group_metrics['standardized_diff'].values,
                'directions': group_metrics['direction'].values,
                'color': get_group_colors().get(group, '#CCCCCC')
            }
    
    # プロット
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. グループ別のボックスプロット（絶対差）
    ax = axes[0, 0]
    box_data = []
    positions = []
    colors = []
    labels = []
    
    for i, (group, data) in enumerate(group_data.items()):
        box_data.append(data['abs_diff'])
        positions.append(i)
        colors.append(data['color'])
        labels.append(f"{group}\n(n={len(data['traits'])})")
    
    bp = ax.boxplot(box_data, positions=positions, widths=0.6, 
                    patch_artist=True, showmeans=True)
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel('Absolute Difference', fontsize=12)
    ax.set_title('Distribution of Differences by Group', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # 2. 方向性の一貫性（どちらの集団が高い傾向にあるか）
    ax = axes[0, 1]
    consistency_data = []
    for group, data in group_data.items():
        # OtherJomon > Iyaiの割合
        consistency = (data['directions'] > 0).sum() / len(data['directions']) * 100
        consistency_data.append(consistency)
    
    bars = ax.bar(positions, consistency_data, color=colors, 
                  alpha=0.7, edgecolor='black', linewidth=1.5)
    
    ax.axhline(y=50, color='red', linestyle='--', alpha=0.5, linewidth=2)
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel('% Traits (OtherJomon > Iyai)', fontsize=12)
    ax.set_title('Directional Consistency', fontsize=13, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.grid(True, alpha=0.3, axis='y')
    
    # パーセンテージを表示
    for bar, pct in zip(bars, consistency_data):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
               f'{pct:.0f}%', ha='center', va='bottom', fontsize=9)
    
    # 3. 変動係数（グループ内のばらつき）
    ax = axes[1, 0]
    cv_data = []
    for group, data in group_data.items():
        cv = np.std(data['abs_diff']) / (np.mean(data['abs_diff']) + 0.01)
        cv_data.append(cv)
    
    bars = ax.bar(positions, cv_data, color=colors, 
                  alpha=0.7, edgecolor='black', linewidth=1.5)
    
    ax.set_xticks(positions)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylabel('Coefficient of Variation', fontsize=12)
    ax.set_title('Within-Group Variability', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    # 4. 散布図：標準化差vs絶対差
    ax = axes[1, 1]
    for group, data in group_data.items():
        ax.scatter(data['abs_diff'], data['std_diff'], 
                  c=data['color'], label=group, s=50, alpha=0.6, 
                  edgecolors='black', linewidth=0.5)
    
    ax.set_xlabel('Absolute Difference', fontsize=12)
    ax.set_ylabel('Standardized Difference', fontsize=12)
    ax.set_title('Absolute vs Standardized Differences', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    
    plt.suptitle(f'Group-Level Variability Analysis (p < {p_value})', 
                fontsize=15, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"グループ変動性プロット保存: {output_path}")

def main():
    # パス設定
    input_dir = "/home/mkato/hdd_data/0_4_analysis/4_PRS/PRS_scores"
    output_dir = "/home/mkato/mkato-jomon/0_4_analysis/4_PRS/plot"
    
    # 出力ディレクトリ作成
    os.makedirs(output_dir, exist_ok=True)
    
    # 入力ファイル一覧取得
    input_files = glob.glob(os.path.join(input_dir, "PRS_scores_p*.tsv"))
    
    print(f"処理対象ファイル数: {len(input_files)}")
    
    # matplotlib設定
    plt.rcParams['font.family'] = 'DejaVu Sans'
    
    # 各ファイルについて処理
    for input_file in input_files:
        filename = os.path.basename(input_file)
        print(f"\n処理中: {filename}")
        
        try:
            # p値を抽出
            p_value = filename.replace('PRS_scores_p', '').replace('.tsv', '')
            
            # データ読み込み
            df = load_prs_data(input_file)
            
            # 差分メトリクスを計算
            metrics_df = calculate_difference_metrics(df)
            
            # 1. 差分ボルケーノプロット
            volcano_output = os.path.join(output_dir, f"PRS_difference_volcano_p{p_value}.png")
            create_difference_volcano(metrics_df, p_value, volcano_output)
            
            # 2. 差分ヒートマップ
            heatmap_output = os.path.join(output_dir, f"PRS_difference_heatmap_p{p_value}.png")
            create_difference_heatmap(metrics_df, p_value, heatmap_output)
            
            # 3. グループ変動性プロット
            variability_output = os.path.join(output_dir, f"PRS_group_variability_p{p_value}.png")
            create_group_variability_plot(metrics_df, p_value, variability_output)
            
            # 統計サマリーを出力
            print(f"\n統計サマリー (p < {p_value}):")
            print(f"  最大差: {metrics_df['absolute_diff'].max():.3f} ({metrics_df['absolute_diff'].idxmax()})")
            print(f"  最小差: {metrics_df['absolute_diff'].min():.3f} ({metrics_df['absolute_diff'].idxmin()})")
            print(f"  中央値: {metrics_df['absolute_diff'].median():.3f}")
            print(f"  OtherJomon > Iyai: {(metrics_df['direction'] > 0).sum()}/{len(metrics_df)} traits")
            
        except Exception as e:
            print(f"エラー: {filename} - {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print("\n全ての処理が完了しました。")

if __name__ == "__main__":
    main()