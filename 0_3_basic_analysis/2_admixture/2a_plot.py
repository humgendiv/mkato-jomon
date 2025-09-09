#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ----- User settings -----
ADMIX_DIR      = "/home/mkato/mkato-jomon/0_3_basic_analysis/2_admixture"
FAM_FILE       = "/home/mkato/hdd_data/0_3_basic_analysis/2_admixture/merged_with_1240K.targetpops.pruned.fam"
PREFIX         = "merged_with_1240K.targetpops.pruned"
OUTPUT_DIR     = os.path.join(ADMIX_DIR, "plots")
Ks             = [3,4]       # 描きたい K 値のリスト
BAR_WIDTH      = 1.0        # バーの幅（統一）

# 3段組みのグループ定義
GROUPS_ROW1 = {
    "Jomon": ["Iyai","Todoroki", "Mitsusawa", "Chidorigakubo", "Funadomari"],
    "Ancient Japanese": ["Japan_Ikawazu_Jomon", "Japan_Sanganji_Jomon", "Japan_KumaNishioda_Yayoi","Japan_Honshu_Kofun"],
    "Modern Japanese & Korean": ["Japanese", "Korean"],
}

GROUPS_ROW2 = {
    "Modern East Asian": ["Ami", "Atayal", "Burmese", "Cambodian", "China_Lahu", "Dai", "Daur", "Han"],
}

GROUPS_ROW3 = {
    "Modern East Asian": ["Hezhen", "Kinh", "Miao", "Mongola", "Naxi", "Oroqen", "She", "Thai", "Tu", "Tujia", "Xibo", "Yi"],
}

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_fam(fam_path: str) -> pd.DataFrame:
    """fam ファイルを読み込んで、一意な sample_id カラムを付与する."""
    cols = ["FID","IID","PID","MID","Sex","Phenotype"]
    df = pd.read_csv(fam_path, sep=r"\s+", header=None, names=cols)
    # 一意化のために "FID:IID" フォーマットで sample_id を作成
    df["sample_id"] = df["FID"].astype(str) + ":" + df["IID"].astype(str)
    return df


def load_qmatrix(q_path: str, sample_index: pd.Index) -> pd.DataFrame:
    """Q 行列を読み込んで、インデックスを sample_id に設定する."""
    q = pd.read_csv(q_path, sep=r"\s+", header=None)
    q.index = sample_index
    return q


def get_samples_for_group(df_fam: pd.DataFrame, pop_list: list[str]) -> list[str]:
    """
    GROUPS の pop_list から、該当する sample_id を
    FID の出現順にまとめて返す。
    """
    samples: list[str] = []
    for pop in pop_list:
        sel = df_fam[df_fam["FID"].astype(str) == pop]
        if sel.empty:
            print(f"  [!] No samples for FID='{pop}'")
        else:
            samples.extend(sel["sample_id"].tolist())
    return samples


def plot_admixture_subplot(ax, q_sub: pd.DataFrame, K: int, title: str, show_ylabel: bool = False):
    """
    指定されたaxesにadmixtureプロットを描画
    """
    n = len(q_sub)
    bottom = np.zeros(n)
    xs = np.arange(n)
    
    # カラーマップの定義（K値に応じて一貫した色を使用）
    if K == 3:
        colors = ["#FF6B6B", '#4ECDC4', '#45B7D1']  # 赤、青緑、青
    elif K == 4:
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']  # 赤、青緑、青、オレンジ
    else:
        colors = plt.cm.Set1(np.linspace(0, 1, K))  # デフォルト
    
    # # stacked bar
    # for k in range(K):
    #     ax.bar(xs, q_sub[k], bottom=bottom, width=BAR_WIDTH, 
    #            color=colors[k], label=f"Cluster {k+1}")
    #     bottom += q_sub[k]
    
    # stacked bar
    for k in range(K):
        ax.bar(xs, q_sub[k], bottom=bottom, width=BAR_WIDTH, 
               label=f"Cluster {k+1}")
        bottom += q_sub[k]

    # 縦軸を0～1に固定
    ax.set_ylim(0, 1)
    
    # y軸の設定
    if show_ylabel:
        ax.set_ylabel("Ancestry Proportion", fontsize=10)
    ax.tick_params(axis='y', labelsize=8)
    
    # 集団ラベル & 境界線用に fid リストを作成
    fids = [samp.split(":", 1)[0] for samp in q_sub.index]
    
    # ラベル表示（最初だけ）
    labels = []
    last = None
    for fid in fids:
        if fid != last:
            labels.append(fid)
        else:
            labels.append("")
        last = fid
    
    ax.set_xticks(xs)
    ax.set_xticklabels(labels, rotation=90, fontsize=9)
    
    # 境界線を引く位置を検出して黒線を追加
    boundaries = []
    last = fids[0]
    for i, fid in enumerate(fids[1:], start=1):
        if fid != last:
            boundaries.append(i - 0.5)
        last = fid
    
    for b in boundaries:
        ax.axvline(x=b, color="k", linewidth=0.8)
    
    # タイトル設定
    ax.set_title(title, fontsize=11, fontweight='bold')
    
    # x軸の範囲を設定（統一感のため）
    ax.set_xlim(-0.5, n - 0.5)


def create_combined_plot(q_mat: pd.DataFrame, fam_df: pd.DataFrame, K: int, output_dir: str):
    """
    3段組みの結合図を作成
    """
    # 各行のデータを準備
    row_data = []
    
    # Row 1
    row1_samples = []
    row1_titles = []
    for grp_name, pop_list in GROUPS_ROW1.items():
        samples = get_samples_for_group(fam_df, pop_list)
        if samples:
            row1_samples.extend(samples)
            row1_titles.append((len(samples), grp_name))
    
    # Row 2
    row2_samples = []
    row2_titles = []
    for grp_name, pop_list in GROUPS_ROW2.items():
        samples = get_samples_for_group(fam_df, pop_list)
        if samples:
            row2_samples.extend(samples)
            row2_titles.append((len(samples), grp_name))
    
    # Row 3
    row3_samples = []
    row3_titles = []
    for grp_name, pop_list in GROUPS_ROW3.items():
        samples = get_samples_for_group(fam_df, pop_list)
        if samples:
            row3_samples.extend(samples)
            row3_titles.append((len(samples), grp_name))
    
    # 最大サンプル数を取得（幅の統一のため）
    max_samples = max(len(row1_samples), len(row2_samples), len(row3_samples))
    
    # 図のサイズ設定
    fig_width = min(20, max(12, max_samples * 0.15))  # 幅は最大20インチに制限
    fig_height = 12  # 3段分の高さを増加
    
    # Figure作成
    fig = plt.figure(figsize=(fig_width, fig_height))
    
    # GridSpecで3行1列のレイアウトを作成（hspaceを増加）
    gs = gridspec.GridSpec(3, 1, figure=fig, hspace=1.0)
    
    # Row 1のプロット
    ax1 = fig.add_subplot(gs[0, 0])
    if row1_samples:
        q_sub1 = q_mat.reindex(row1_samples)
        # タイトルを結合
        title1 = " | ".join([t[1] for t in row1_titles])
        plot_admixture_subplot(ax1, q_sub1, K, title1, show_ylabel=False)
    
    # Row 2のプロット
    ax2 = fig.add_subplot(gs[1, 0])
    if row2_samples:
        q_sub2 = q_mat.reindex(row2_samples)
        title2 = " | ".join([t[1] for t in row2_titles])
        plot_admixture_subplot(ax2, q_sub2, K, title2, show_ylabel=False)
    
    # Row 3のプロット
    ax3 = fig.add_subplot(gs[2, 0])
    if row3_samples:
        q_sub3 = q_mat.reindex(row3_samples)
        title3 = " | ".join([t[1] for t in row3_titles])
        plot_admixture_subplot(ax3, q_sub3, K, title3, show_ylabel=False)
    
    # 全体のタイトル
    fig.suptitle(f'ADMIXTURE Analysis (K={K})', fontsize=14, fontweight='bold', y=0.98)
    
    # レジェンドを図の右側に配置
    #handles, labels = ax1.get_legend_handles_labels()
    #fig.legend(handles, labels, loc='center right', bbox_to_anchor=(0.98, 0.5), 
    #           fontsize=10, title='Clusters')
    
    # レイアウト調整（上下の余白も調整）
    plt.tight_layout(rect=[0, 0.02, 0.92, 0.96])
    
    # 保存
    out_png = os.path.join(output_dir, f"admixture_K{K}_combined.png")
    fig.savefig(out_png, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved combined plot → {out_png}")


def main():
    fam_df = load_fam(FAM_FILE)
    # 全サンプル順のインデックス
    all_samples = fam_df["sample_id"]
    
    for K in Ks:
        q_path = os.path.join(ADMIX_DIR, f"{PREFIX}.{K}.Q")
        if not os.path.exists(q_path):
            print(f"[Warning] {q_path} not found, skipping K={K}")
            continue
        
        print(f"\nProcessing K={K}...")
        q_mat = load_qmatrix(q_path, all_samples)
        
        # 結合図を作成
        create_combined_plot(q_mat, fam_df, K, OUTPUT_DIR)


if __name__ == "__main__":
    main()