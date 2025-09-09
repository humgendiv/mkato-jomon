#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
draw_f3_maps_paper.py
  • 各 Jomon 個体の f3 を日本地図で可視化
  • 論文掲載用: 5集団の地図を2行3列で結合（各地図は独自カラースケール）
  • 上段3つ、下段2つ（中央寄せ）のレイアウト
依存: pandas, matplotlib, japanmap
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.gridspec import GridSpec
from japanmap import picture

# ---------- 設定 ----------
F3_FILE = "/home/mkato/mkato-jomon/0_4_analysis/3_prefecture/outgroup_f3_3x47.tsv"
OUTDIR  = "/home/mkato/mkato-jomon/0_4_analysis/3_prefecture/maps"
CMAP    = "Reds"      # 連続カラーマップ
FIGSIZE_PAPER = (16, 10)   # 2行3列用のサイズ（少し横幅を増やす）
# -------------------------

os.makedirs(OUTDIR, exist_ok=True)
df = pd.read_csv(F3_FILE, sep="\t")

# kenXX → 1–47
df["pref_code"] = df["Prefecture"].str.extract(r"ken(\d+)").astype(int)

# Jomonリストを時代順に定義
jomon_order = ["Iyai", "Todoroki", "Mitsusawa", "Chidorigakubo", "Funadomari"]

# データに存在する集団のみを使用
available_jomon = list(df["Jomon"].unique())
jomon_list = [j for j in jomon_order if j in available_jomon]

# 存在しない集団があれば警告
missing = [j for j in jomon_order if j not in available_jomon]
if missing:
    print(f"Warning: Following groups not found in data: {missing}")

n_jomon = len(jomon_list)

# データが5集団でない場合の確認
if n_jomon != 5:
    print(f"Warning: Expected 5 Jomon groups, but found {n_jomon}")
    # データにない集団がある場合は利用可能な集団のみ使用

# ========== 論文用: 2行3列配置（3+2、各地図は独自カラースケール） ==========
fig = plt.figure(figsize=FIGSIZE_PAPER)

# GridSpecで上段3つ、下段2つ（中央寄せ）のレイアウトを作成
# wspaceを増やして図間の余白を確保
gs = GridSpec(2, 6, figure=fig, hspace=0.3, wspace=0.5)

# 軸の配置
# 上段: 3つ（各2列分を使用）
axes = []
axes.append(fig.add_subplot(gs[0, 0:2]))  # 上段左
axes.append(fig.add_subplot(gs[0, 2:4]))  # 上段中央
axes.append(fig.add_subplot(gs[0, 4:6]))  # 上段右
# 下段: 2つ（中央寄せ、各2列分を使用）
axes.append(fig.add_subplot(gs[1, 1:3]))  # 下段左寄り
axes.append(fig.add_subplot(gs[1, 3:5]))  # 下段右寄り

cmap = plt.get_cmap(CMAP)

for idx, (ax, jomon) in enumerate(zip(axes[:n_jomon], jomon_list)):
    sub = df[df["Jomon"] == jomon]
    
    # ★★ 各集団ごとの独自スケール ★★
    vmin_local = sub["f3"].min()
    vmax_local = sub["f3"].max()
    norm_local = colors.Normalize(vmin=vmin_local, vmax=vmax_local, clip=True)
    
    # 色設定は独自スケールに基づく
    color_dict = {
        row.pref_code: colors.rgb2hex(cmap(norm_local(row.f3)))
        for row in sub.itertuples()
    }
    img = picture(color_dict)
    
    # 地図をプロット
    ax.imshow(img)
    ax.axis("off")
    ax.set_title(jomon, fontsize=14, fontweight='bold', pad=10)
    
    # 各地図に独自スケールのカラーバー
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="8%", pad=0.05)
    
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm_local)
    sm.set_array([])
    cbar = fig.colorbar(sm, cax=cax)
    cbar.ax.tick_params(labelsize=9)
    
    # カラーバーのラベル
    #cbar.set_label("f3", rotation=0, labelpad=15, fontsize=10)
    
    # カラーバーの値を小数表示でフォーマット（論文用）
    # 指数表示を避け、小数点以下3桁で表示
    import matplotlib.ticker as ticker
    cbar.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
    cbar.update_ticks()
    
    print(f"✓ {jomon}: vmin={vmin_local:.4f}, vmax={vmax_local:.4f}")

# 全体のタイトル
fig.suptitle("Outgroup f3(Jomon, Modern Japanese; Mbuti)", 
             fontsize=16, fontweight='bold', y=0.98)

# 保存
paper_png = os.path.join(OUTDIR, "Jomon_f3_prefecture_paper_2x3.png")
fig.savefig(paper_png, dpi=300, bbox_inches='tight')
plt.close(fig)

print(f"\n✓ 論文用結合画像出力: {paper_png}")

# ========== オプション: 個別PNG（各集団ごとの独自スケール）も出力 ==========
SAVE_INDIVIDUAL = True  # 個別画像も保存する場合はTrue

if SAVE_INDIVIDUAL:
    FIGSIZE_SINGLE = (5, 8)  # 少し大きめに
    
    for jomon, sub in df.groupby("Jomon", sort=False):
        vmin_local = sub["f3"].min()
        vmax_local = sub["f3"].max()
        norm_local = colors.Normalize(vmin=vmin_local, vmax=vmax_local, clip=True)
        
        color_dict = {
            row.pref_code: colors.rgb2hex(cmap(norm_local(row.f3)))
            for row in sub.itertuples()
        }
        img = picture(color_dict)

        fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
        ax.imshow(img)
        ax.axis("off")
        ax.set_title(f"{jomon}\nf3(Jomon, Modern Japanese; Mbuti)", 
                    fontsize=12, fontweight='bold')

        # 独自スケールのカラーバー
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm_local)
        sm.set_array([])
        cbar = fig.colorbar(sm, ax=ax, fraction=0.045, pad=0.02)
        cbar.set_label("f3", rotation=0, labelpad=12)
        cbar.ax.tick_params(labelsize=9)

        # カラーバーの値を小数表示でフォーマット
        import matplotlib.ticker as ticker
        cbar.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
        cbar.update_ticks()
        fig.tight_layout()
        fig.savefig(out_png, dpi=300, bbox_inches='tight')
        plt.close(fig)
        print(f"✓ 個別画像: {out_png}")

print("\n完了しました。")