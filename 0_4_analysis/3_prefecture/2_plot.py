#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
draw_f3_maps_shared.py
  • 各 Jomon 個体の f3 を日本地図で可視化
  • 全個体で共通のカラースケール
  • ① 個別 PNG（色対応統一） ② 2×3 サブプロット PNG（共有カラーバー） を出力
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

# ★★ 共有スケール ★★
vmin_global, vmax_global = df["f3"].min(), df["f3"].max()
norm_global = colors.Normalize(vmin=vmin_global, vmax=vmax_global, clip=True)
cmap = plt.get_cmap(CMAP)

# ========== ① 個別 PNG ==========
for jomon, sub in df.groupby("Jomon", sort=False):
    # 色設定は共有スケールに基づく
    color_dict = {
        row.pref_code: colors.rgb2hex(cmap(norm_global(row.f3)))
        for row in sub.itertuples()
    }
    img = picture(color_dict)

    fig, ax = plt.subplots(figsize=FIGSIZE_SINGLE)
    ax.imshow(img)
    ax.axis("off")
    ax.set_title(f"{jomon}  f3(Jomon, Modern Japanese; Mbuti)")

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm_global)
    sm.set_array([])
    cbar = fig.colorbar(sm, ax=ax, fraction=0.04, pad=0.02)
    cbar.set_label("f3", rotation=0, labelpad=10)
    cbar.ax.tick_params(labelsize=8)

    out_png = os.path.join(OUTDIR, f"{jomon}_f3_prefecture_sharedscale.png")
    fig.tight_layout()
    fig.savefig(out_png, dpi=300)
    plt.close(fig)
    print(f"✓  {out_png} 出力")

# ========== ② 6 枚まとめたサブプロット ==========
jomon_list = list(df["Jomon"].unique())
nrow, ncol = 2, 3
fig, axes = plt.subplots(nrow, ncol, figsize=FIGSIZE_COMBO)

for ax, jomon in zip(axes.flat, jomon_list):
    sub = df[df["Jomon"] == jomon]
    color_dict = {
        row.pref_code: colors.rgb2hex(cmap(norm_global(row.f3)))
        for row in sub.itertuples()
    }
    ax.imshow(picture(color_dict))
    ax.axis("off")
    ax.set_title(jomon)

# # 共通カラーバー（図全体で 1 本）
# sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm_global)
# sm.set_array([])
# cbar = fig.colorbar(sm, ax=axes.ravel().tolist(),
#                     fraction=0.025, pad=0.02)
# cbar.set_label("f3", rotation=0, labelpad=10)
# cbar.ax.tick_params(labelsize=8)

cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])   # 右端中央に縦長  (調整可)

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
print(f"✓  {combo_png} 出力\n共有スケール vmin={vmin_global:.4f}, vmax={vmax_global:.4f}")
