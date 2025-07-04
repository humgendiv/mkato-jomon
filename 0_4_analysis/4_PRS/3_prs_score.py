"""

/home/mkato/hdd_data/0_4_analysis/4_PRS/alfreq.tsvと、
/home/mkato/hdd_data/0_4_analysis/4_PRS/PRS_processed内にある各形質のGWASファイルを用いて、
各形質における各集団(alfreq.tsvにおける3集団)のPRSを計算していく。
結果は、/home/mkato/hdd_data/0_4_analysis/4_PRS/PRS_scoresに保存する。
各形質は、ファイル名に含まれている。ドット(.)区切りの2番目の要素、またはアンダースコア(_)区切りの3番目の要素が形質名となる。アンダースコアがファイル名に含まれなければ自動的にドット区切りであると判断してよい。
PRS計算に際しては、p値に基づく閾値を3種類設定し、それ以下のSNPのみ計算対象とする。閾値は0.01, 0.001, 0.0001の3つとする。
PRSはアリル頻度とBETAをかけ合わせ、各SNPの値を合計することで計算される。
GWASファイルとアリル頻度ファイルで同一のSNPを見つけるとき、IDだけでなくREFとALTの一致も確認し、不一致であれば計算対象から除外する。
計算結果を書き込むファイルは、列を集団名、行をtrait名とし、各セルにPRS値を格納するタブ区切りファイルとする。

"""

import os
import pandas as pd
import glob

def load_allele_frequencies(file_path):
    """アリル頻度ファイルを読み込み"""
    df = pd.read_csv(file_path, sep='\t')
    return df

def extract_trait_name(filename):
    """ファイル名から形質名を抽出"""
    basename = os.path.basename(filename)
    
    # 特殊ケースの処理
    if 'Height' in basename:
        return 'Height'
    elif 'BMI' in basename:
        return 'BMI'
    
    # 標準的なBBJファイル名の処理
    if basename.startswith('BBJ.') and basename.endswith('.autosome.txt'):
        # BBJ.HDL-C.autosome.txt -> HDL-C
        return basename.replace('BBJ.', '').replace('.autosome.txt', '')
    
    # アンダースコア区切りの場合
    if '_' in basename:
        parts = basename.split('_')
        if len(parts) >= 3:
            return parts[2]
    
    # ドット区切りの場合
    if '.' in basename:
        parts = basename.split('.')
        if len(parts) >= 2:
            return parts[1]
    
    return basename

def load_gwas_file(file_path):
    """GWASファイルを読み込み"""
    df = pd.read_csv(file_path, sep='\t')
    return df

def calculate_prs(allele_freq_df, gwas_df, populations, p_thresholds):
    """PRS計算"""
    results = {}
    
    # 各p値閾値について計算
    for p_threshold in p_thresholds:
        # p値でフィルタリング
        filtered_gwas = gwas_df[gwas_df['P'] <= p_threshold].copy()
        
        # アリル頻度データとGWASデータをマージ
        merged = pd.merge(
            allele_freq_df, 
            filtered_gwas, 
            left_on=['ID', 'REF', 'ALT'], 
            right_on=['ID', 'REF', 'ALT'],
            how='inner'
        )
        
        # 各集団についてPRS計算
        prs_scores = {}
        for pop in populations:
            if pop in merged.columns:
                # PRS = sum(allele_frequency * beta)
                prs_score = (merged[pop] * merged['BETA']).sum()
                prs_scores[pop] = prs_score
        
        results[p_threshold] = prs_scores
    
    return results

def main():
    # パス設定
    allele_freq_file = "/home/mkato/hdd_data/0_4_analysis/4_PRS/alfreq.tsv"
    gwas_dir = "/home/mkato/hdd_data/0_4_analysis/4_PRS/PRS_processed"
    output_dir = "/home/mkato/hdd_data/0_4_analysis/4_PRS/PRS_scores"
    
    # 出力ディレクトリ作成
    os.makedirs(output_dir, exist_ok=True)
    
    # p値閾値設定
    p_thresholds = [0.01, 0.001, 0.0001]
    
    # アリル頻度データ読み込み
    print("アリル頻度データを読み込み中...")
    allele_freq_df = load_allele_frequencies(allele_freq_file)
    populations = ['Iyai', 'OtherJomon', 'ModernJapanese']
    
    print(f"アリル頻度データ: {len(allele_freq_df)} variants")
    print(f"集団: {populations}")
    
    # GWASファイル一覧取得
    gwas_files = glob.glob(os.path.join(gwas_dir, "*.txt"))
    print(f"GWASファイル数: {len(gwas_files)}")
    
    # 各p値閾値について結果を格納するデータフレームを初期化
    results_dfs = {}
    for p_threshold in p_thresholds:
        results_dfs[p_threshold] = pd.DataFrame(columns=populations)
    
    # 各GWASファイルについて処理
    for gwas_file in gwas_files:
        trait_name = extract_trait_name(gwas_file)
        print(f"処理中: {trait_name}")
        
        try:
            # GWASデータ読み込み
            gwas_df = load_gwas_file(gwas_file)
            
            # PRS計算
            prs_results = calculate_prs(allele_freq_df, gwas_df, populations, p_thresholds)
            
            # 結果を各データフレームに追加
            for p_threshold in p_thresholds:
                results_dfs[p_threshold].loc[trait_name] = prs_results[p_threshold]
                
        except Exception as e:
            print(f"エラー: {trait_name} - {str(e)}")
            continue
    
    # 各p値閾値について結果を保存
    for p_threshold in p_thresholds:
        output_file = os.path.join(output_dir, f"PRS_scores_p{p_threshold}.tsv")
        results_dfs[p_threshold].to_csv(output_file, sep='\t', index=True)
        print(f"保存完了: {output_file}")
    
    print("全ての処理が完了しました。")

if __name__ == "__main__":
    main()