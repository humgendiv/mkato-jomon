#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
draw_f3_maps_individual.py
  • 各 Jomon 個体の f3 を日本地図で可視化
  • ① 個別 PNG（各集団ごとの独自カラースケール）
  • ② 2×3 サブプロット PNG（共有カラーバー）を出力
依存: pandas, matplotlib, japanmap
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
from japanmap import picture

# ---------- 設定 ----------
F3_FILE = "/home/mkato/mkato-jomon/0_4_analysis/3_prefecture/outgroup_f3_3x47.tsv"
OUTDIR  = "/home/mkato/mkato-jomon/0_4_analysis/3_prefecture/maps"
CMAP    = "Reds"      # 連続カラーマップ
FIGSIZE_SINGLE = (4, 8)
FIGSIZE_COMBO  = (12, 8)   # 2×3 配置
# -------------------------

os.makedirs(OUTDIR, exist_ok=True)
df = pd.read_csv(F3_FILE, sep="\t")

# kenXX → 1–47
df["pref_code"] = df["Prefecture"].str.extract(r"ken(\d+)").astype(int)

# 全体の共有スケール（結合プロット用）
vmin_global, vmax_global = df["f3"].min(), df["f3"].max()
norm_global = colors.Normalize(vmin=vmin_global, vmax=vmax_global, clip=True)
cmap = plt.get_cmap(CMAP)

# ========== ① 個別 PNG（各集団ごとの独自スケール） ==========
for jomon, sub in df.groupby("Jomon", sort=False):
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

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
    ax.imshow(img)
    ax.axis("off")
    ax.set_title(f"{jomon}  f3(Jomon, Modern Japanese; Mbuti)")

    # 独自スケールのカラーバー
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm_local)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, fraction=0.04, pad=0.02)
    cbar.set_label("f3", rotation=0, labelpad=10)
    cbar.ax.tick_params(labelsize=8)

    out_png = os.path.join(OUTDIR, f"{jomon}_f3_prefecture_individualscale.png")
    fig.tight_layout()
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    print(f"✓  {out_png} 出力 (vmin={vmin_local:.4f}, vmax={vmax_local:.4f})")

# ========== ② 6 枚まとめたサブプロット（共有スケール） ==========
jomon_list = list(df["Jomon"].unique())
nrow, ncol = 2, 3
fig, axes = plt.subplots(nrow, ncol, figsize=FIGSIZE_COMBO)

for ax, jomon in zip(axes.flat, jomon_list):
    sub = df[df["Jomon"] == jomon]
    # 結合プロットでは共有スケールを使用
    color_dict = {
        row.pref_code: colors.rgb2hex(cmap(norm_global(row.f3)))
        for row in sub.itertuples()
    }
    ax.imshow(picture(color_dict))
    ax.axis("off")
    ax.set_title(jomon)

# 共通カラーバー（図全体で 1 本）
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])   # 右端中央に縦長

sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm_global)
sm.set_array([])

fig.colorbar(sm, cax=cbar_ax)
cbar_ax.set_title("f3", pad=4, fontsize=10)
cbar_ax.tick_params(labelsize=8)

fig.suptitle("Outgroup f3(Jomon,Modern Japanese; Mbuti)  –  shared colour scale", fontsize=14)
fig.tight_layout(rect=[0, 0, 0.9, 0.96])  # ← right=0.9 で地図を少し左に寄せる

combo_png = os.path.join(OUTDIR, "Jomon_f3_prefecture_combined_sharedscale.png")
fig.savefig(combo_png, dpi=300)
plt.close(fig)
print(f"✓  {combo_png} 出力")
print(f"共有スケール vmin={vmin_global:.4f}, vmax={vmax_global:.4f}")