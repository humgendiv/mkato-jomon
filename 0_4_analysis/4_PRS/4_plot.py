"""
PRSの計算結果をプロットする。
PRSは、IyaiとOtherJomonの値に対して、ModernJapaneseの値を引くことで現代人との差を可視化する。
traitは、平均値でsortし、平均値が高いものを上に表示する。
2集団は色を分けてわかりやすく表示する。
入力ファイルは、/home/mkato/hdd_data/0_4_analysis/4_PRS/PRS_scores内に3ファイルあるのでそれぞれに対してプロットする。
出力は、/home/mkato/mkato-jomon/0_4_analysis/4_PRS/plot内に保存する。
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob

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
    
    # プロット設定
    fig, ax = plt.subplots(figsize=(10, max(8, len(sorted_df) * 0.5)))
    
    # Y軸の位置
    y_pos = np.arange(len(sorted_df))
    
    # プロット作成
    width = 0.35
    bars1 = ax.barh(y_pos - width/2, sorted_df['Iyai'], width, 
                   label='Iyai', color='#2E8B57', alpha=0.8)
    bars2 = ax.barh(y_pos + width/2, sorted_df['OtherJomon'], width, 
                   label='OtherJomon', color='#CD853F', alpha=0.8)
    
    # 軸設定
    ax.set_yticks(y_pos)
    ax.set_yticklabels(sorted_df.index)
    ax.set_xlabel('PRS Difference from Modern Japanese')
    ax.set_title(f'PRS Differences (p < {p_value})')
    ax.legend()
    
    # ゼロライン
    ax.axvline(x=0, color='black', linestyle='--', alpha=0.5)
    
    # グリッド
    ax.grid(True, alpha=0.3)
    
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
            output_file = os.path.join(output_dir, f"PRS_differences_p{p_value}.png")
            create_plot(diff_df, p_value, output_file)
            
        except Exception as e:
            print(f"エラー: {filename} - {str(e)}")
            continue
    
    print("全ての処理が完了しました。")

if __name__ == "__main__":
    main()