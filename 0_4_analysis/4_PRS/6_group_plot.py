"""
PRSの計算結果を形質群（臓器・機能）ごとに集計して可視化する。
4a_plot.pyの色分けとグループ分けに完全に準拠。
入力ファイルは、/home/mkato/hdd_data/0_4_analysis/4_PRS/PRS_scores内に3ファイルあるのでそれぞれに対してプロットする。
出力は、/home/mkato/mkato-jomon/0_4_analysis/4_PRS/plot内に保存する。
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
from scipy import stats

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

def assign_trait_groups(traits):
    """各指標をグループに割り当て"""
    groups = get_trait_groups()
    
    trait_groups = {}
    
    # 各指標をグループに割り当て
    for trait in traits:
        assigned = False
        for group_name, group_traits in groups.items():
            if trait in group_traits:
                trait_groups[trait] = group_name
                assigned = True
                break
        
        if not assigned:
            trait_groups[trait] = 'Other'
    
    return trait_groups

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
        'OtherJomon': other_jomon_diff
    })
    
    return diff_df

def calculate_fold_change(iyai_val, other_val, epsilon=0.1):
    """Fold Changeを計算"""
    # 両方の値が小さい場合
    if abs(iyai_val) < epsilon and abs(other_val) < epsilon:
        return 1.0
    # Iyaiがゼロに近い場合
    elif abs(iyai_val) < epsilon:
        return np.sign(other_val) * abs(other_val) / epsilon
    else:
        return other_val / iyai_val

def calculate_group_statistics(diff_df):
    """グループごとの統計量を計算"""
    # 指標のグループを取得
    trait_groups = assign_trait_groups(diff_df.index)
    groups = get_trait_groups()
    colors = get_group_colors()
    
    # グループごとにデータを集計
    group_stats = {}
    
    for group_name in list(groups.keys()) + ['Other']:
        # このグループに属する指標を抽出
        group_traits = [t for t, g in trait_groups.items() if g == group_name]
        
        if group_traits:
            # グループのデータを抽出
            group_iyai = diff_df.loc[group_traits, 'Iyai']
            group_other = diff_df.loc[group_traits, 'OtherJomon']
            
            # Fold Changeを計算
            fold_changes = []
            for trait in group_traits:
                fc = calculate_fold_change(
                    diff_df.loc[trait, 'Iyai'],
                    diff_df.loc[trait, 'OtherJomon']
                )
                fold_changes.append(fc)
            
            log2_fc = np.log2(np.abs(fold_changes)) * np.sign(fold_changes)
            log2_fc = np.clip(log2_fc, -8, 8)
            
            # 効果量を計算
            diff_magnitude = np.abs(group_other - group_iyai)
            mean_abs_diff = np.mean(np.abs(np.concatenate([
                diff_df['Iyai'].values, 
                diff_df['OtherJomon'].values
            ])))
            
            if mean_abs_diff > 0:
                effect_sizes = diff_magnitude / mean_abs_diff
            else:
                effect_sizes = diff_magnitude
            
            # 統計量を計算
            stats = {
                'n': len(group_traits),
                'mean_log2FC': np.mean(log2_fc),
                'std_log2FC': np.std(log2_fc),
                'median_log2FC': np.median(log2_fc),
                'mean_effect': np.mean(effect_sizes),
                'std_effect': np.std(effect_sizes),
                'median_effect': np.median(effect_sizes),
                # 方向性の一貫性（OtherJomon > Iyaiの割合）
                'consistency': (np.array(log2_fc) > 0).sum() / len(group_traits),
                # 各形質の値も保存（詳細分析用）
                'traits': group_traits,
                'log2_fc_values': log2_fc,
                'effect_values': effect_sizes
            }
            
            # 色を取得
            if group_name != 'Other':
                stats['color'] = colors[group_name]
            else:
                stats['color'] = '#CCCCCC'
                
            group_stats[group_name] = stats
    
    return group_stats

def create_group_summary_plot(group_stats, p_value, output_path):
    """形質群ごとの傾向を示すサマリープロット"""
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
    ax1.axvline(x=-1, color='gray', linestyle='--', alpha=0.4)
    ax1.axvline(x=1, color='gray', linestyle='--', alpha=0.4)
    
    ax1.set_xlabel('Mean Log2 Fold Change (OtherJomon / Iyai)', fontsize=12)
    ax1.set_ylabel('Mean Effect Size', fontsize=12)
    ax1.set_title(f'Group-level Summary (p < {p_value})', fontsize=14)
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10, framealpha=0.9, loc='best')
    
    # 軸のスタイル
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
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
    bars = ax2.bar(range(len(group_names)), consistencies, color=bar_colors, 
                   alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # 50%ライン
    ax2.axhline(y=50, color='red', linestyle='--', alpha=0.7, linewidth=2)
    
    ax2.set_xticks(range(len(group_names)))
    ax2.set_xticklabels(group_names, fontsize=11)
    ax2.set_ylabel('Traits with OtherJomon > Iyai (%)', fontsize=12)
    ax2.set_title('Directional Consistency by Group', fontsize=14)
    ax2.set_ylim(0, 100)
    ax2.grid(True, alpha=0.3, axis='y')
    
    # 軸のスタイル
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
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
    print(f"\nグループ別統計 (p < {p_value}):")
    for group_name in ordered_groups:
        stats = group_stats[group_name]
        print(f"  {group_name}: n={stats['n']}, "
              f"mean_log2FC={stats['mean_log2FC']:.2f}±{stats['std_log2FC']:.2f}, "
              f"mean_effect={stats['mean_effect']:.2f}±{stats['std_effect']:.2f}, "
              f"OtherJomon>Iyai={stats['consistency']*100:.1f}%")

def create_boxplot_by_group(group_stats, p_value, output_path):
    """グループ別のボックスプロットを作成（追加の可視化）"""
    # プロット作成
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # データを準備
    ordered_groups = [g for g in group_stats.keys() if g != 'Other']
    if 'Other' in group_stats:
        ordered_groups.append('Other')
    
    # Log2 Fold Changeのボックスプロット
    log2fc_data = []
    effect_data = []
    positions = []
    colors = []
    
    for i, group_name in enumerate(ordered_groups):
        stats = group_stats[group_name]
        log2fc_data.append(stats['log2_fc_values'])
        effect_data.append(stats['effect_values'])
        positions.append(i)
        colors.append(stats['color'])
    
    # ボックスプロット（Log2 FC）
    bp1 = ax1.boxplot(log2fc_data, positions=positions, widths=0.6, patch_artist=True,
                      showmeans=True, meanline=True)
    
    # 色を設定
    for patch, color in zip(bp1['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax1.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    ax1.set_xticks(positions)
    ax1.set_xticklabels([f"{g}\n(n={group_stats[g]['n']})" for g in ordered_groups])
    ax1.set_ylabel('Log2 Fold Change (OtherJomon / Iyai)', fontsize=12)
    ax1.set_title(f'Distribution of Log2 Fold Changes by Group (p < {p_value})', fontsize=14)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # ボックスプロット（Effect Size）
    bp2 = ax2.boxplot(effect_data, positions=positions, widths=0.6, patch_artist=True,
                      showmeans=True, meanline=True)
    
    # 色を設定
    for patch, color in zip(bp2['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax2.axhline(y=0.5, color='gray', linestyle='--', alpha=0.5, label='Small effect')
    ax2.axhline(y=1.0, color='gray', linestyle=':', alpha=0.5, label='Medium effect')
    ax2.set_xticks(positions)
    ax2.set_xticklabels([f"{g}\n(n={group_stats[g]['n']})" for g in ordered_groups])
    ax2.set_ylabel('Effect Size', fontsize=12)
    ax2.set_title('Distribution of Effect Sizes by Group', fontsize=14)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.legend(fontsize=10, framealpha=0.9)
    
    # スタイル調整
    for ax in [ax1, ax2]:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"ボックスプロット保存: {output_path}")

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
        print(f"\n処理中: {filename}")
        
        try:
            # p値を抽出
            p_value = filename.replace('PRS_scores_p', '').replace('.tsv', '')
            
            # データ読み込み
            df = load_prs_data(input_file)
            
            # 差分計算
            diff_df = calculate_differences(df)
            
            # グループ統計量を計算
            group_stats = calculate_group_statistics(diff_df)
            
            # グループサマリープロット作成
            summary_output = os.path.join(output_dir, f"PRS_group_summary_p{p_value}.png")
            create_group_summary_plot(group_stats, p_value, summary_output)
            
            # ボックスプロット作成（追加の可視化）
            boxplot_output = os.path.join(output_dir, f"PRS_group_boxplot_p{p_value}.png")
            create_boxplot_by_group(group_stats, p_value, boxplot_output)
            
        except Exception as e:
            print(f"エラー: {filename} - {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print("\n全ての処理が完了しました。")

if __name__ == "__main__":
    main()