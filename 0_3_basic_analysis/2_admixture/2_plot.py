#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----- User settings -----
ADMIX_DIR      = "/home/mkato/mkato-jomon/0_3_basic_analysis/2_admixture"
FAM_FILE       = "/home/mkato/hdd_data/0_3_basic_analysis/2_admixture/merged_with_1240K.targetpops.pruned.fam"
PREFIX         = "merged_with_1240K.targetpops.pruned"
OUTPUT_DIR     = os.path.join(ADMIX_DIR, "plots")
Ks             = [3,]       # 描きたい K 値のリスト
BAR_WIDTH_INCH = 0.25      # １本あたりのバー幅（inch）

# グループ定義: {出力ファイル名: [含めたい FID のリスト]}
GROUPS = {
    "Jomon": ["Iyai","Todoroki", "Mitsusawa", "Chidorigakubo", "Funadomari", ],
    "Ancient Japanese & Korean": ["Japan_Rokutsu_Jomon", "Japan_Honshu_EarlyJomon", "Japan_Honshu_MidLateJomon", "Japan_Ikawazu_Jomon", "Japan_Sanganji_Jomon", "Japan_Shikoku_InitialJomon", "Japan_Shikoku_LateJomon", "Japan_KumaNishioda_Yayoi","Japan_Honshu_Kofun"],
    "Japanese & Korean": ["Japanese", "Korean"],
    "Modern East Asian": ["Ami", "Atayal", "Burmese", "Cambodian", "China_Lahu", "Dai", "Daur", "Han"],
    "Modern East Asian2":  ["Hezhen", "Kinh", "Miao", "Mongola", "Naxi", "Oroqen", "She", "Thai", "Tu", "Tujia", "Xibo", "Yi"],
    # 他の組み合わせを追加したい場合はここに書き足してください
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


def plot_admixture(
    q_sub: pd.DataFrame,
    K: int,
    grp_name: str,
    out_dir: str,
    bar_width_inch: float = 0.25
):
    """部分 Q 行列（q_sub）を stacked barplot してファイル出力."""
    n = len(q_sub)
    fig_w = n * bar_width_inch
    fig_h = 5

    fig, ax = plt.subplots(figsize=(fig_w, fig_h))
    bottom = np.zeros(n)
    xs = np.arange(n)

    # stacked bar
    for k in range(K):
        ax.bar(xs, q_sub[k], bottom=bottom, width=1.0, label=f"Cluster {k+1}")
        bottom += q_sub[k]
        # 【ここを追加】縦軸を 0～1 に固定
    ax.set_ylim(0, 1)

    # 3) 集団ラベル & 境界線用に fid リストを作成
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
    ax.set_xticklabels(labels, rotation=90, fontsize=6)

    # 4) 境界線を引く位置を検出して黒線を追加
    boundaries = []
    last = fids[0]
    for i, fid in enumerate(fids[1:], start=1):
        if fid != last:
            # i番目のバーの左端（i-0.5）に線を引く
            boundaries.append(i - 0.5)
        last = fid

    for b in boundaries:
        ax.axvline(x=b, color="k", linewidth=0.8)

    #ax.set_title(f"{grp_name}")
    ax.tick_params(axis='y', which='both', labelleft=False)

    plt.tight_layout()

    out_png = os.path.join(out_dir, f"admixture_K{K}_{grp_name}.png")
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    print(f"  Saved → {out_png}")


def main():
    fam_df = load_fam(FAM_FILE)
    # 全サンプル順のインデックス
    all_samples = fam_df["sample_id"]

    for K in Ks:
        q_path = os.path.join(ADMIX_DIR, f"{PREFIX}.{K}.Q")
        if not os.path.exists(q_path):
            print(f"[Warning] {q_path} not found, skipping K={K}")
            continue

        q_mat = load_qmatrix(q_path, all_samples)

        for grp_name, pop_list in GROUPS.items():
            samples_sub = get_samples_for_group(fam_df, pop_list)
            if not samples_sub:
                print(f"  [!] Group '{grp_name}' has no samples, skipping.")
                continue

            # インデックス順に再構成
            q_sub = q_mat.reindex(samples_sub)

            plot_admixture(
                q_sub   = q_sub,
                K       = K,
                grp_name= grp_name,
                out_dir = OUTPUT_DIR,
                bar_width_inch= BAR_WIDTH_INCH
            )

if __name__ == "__main__":
    main()
