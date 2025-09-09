#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
draw_f3_maps_with_sites.py
  • 各 Jomon 個体の f3 を日本地図で可視化
  • 論文掲載用: 5集団の地図を2行3列で結合（共通カラースケール）
  • 各地図にサンプル出土地点をプロット
依存: pandas, matplotlib, japanmap
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.gridspec import GridSpec
from japanmap import picture
import numpy as np

# ---------- 設定 ----------
F3_FILE = "/home/mkato/mkato-jomon/0_4_analysis/3_prefecture/outgroup_f3_3x47.tsv"
OUTDIR  = "/home/mkato/mkato-jomon/0_4_analysis/3_prefecture/maps"

# カラーマップの選択肢
CMAP_OPTIONS = {
    "diverging": "RdBu_r",      # 赤-白-青の発散型
    "terrain": "terrain",        # 地形図風
    "viridis": "viridis",        # 連続的な変化
    "coolwarm": "coolwarm",      # 寒暖色
    "RdYlBu": "RdYlBu_r",       # 赤-黄-青
    "Spectral": "Spectral_r"    # スペクトル
}

SELECTED_CMAP = "RdBu_r"  # 使用するカラーマップ
FIGSIZE_PAPER = (16, 10)   # 2行3列用のサイズ

# サンプル出土地点の座標（緯度、経度）
# japanmapの画像座標系に変換するための概算値
SITE_LOCATIONS = {
    "Funadomari": {
        "name": "礼文島",
        "lat": 45.30, "lon": 141.05,  # 北海道礼文島
        "img_x": 0.12, "img_y": 0.02  # 画像上の相対位置
    },
    "Todoroki": {
        "name": "宇土市",
        "lat": 32.69, "lon": 130.66,  # 熊本県宇土市
        "img_x": 0.08, "img_y": 0.82  # 画像上の相対位置
    },
    "Iyai": {
        "name": "長野原町",
        "lat": 36.56, "lon": 138.65,  # 群馬県吾妻郡長野原町
        "img_x": 0.70, "img_y": 0.50  # 画像上の相対位置
    },
    "Mitsusawa": {
        "name": "横浜市",
        "lat": 35.47, "lon": 139.62,  # 神奈川県横浜市
        "img_x": 0.80, "img_y": 0.60  # 画像上の相対位置
    },
    "Chidorigakubo": {
        "name": "大田区",
        "lat": 35.58, "lon": 139.70,  # 東京都大田区
        "img_x": 0.80, "img_y": 0.59  # 画像上の相対位置
    }
}
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
n_jomon = len(jomon_list)

# ========== 共通スケールの設定 ==========
vmin_global = df["f3"].min()
vmax_global = df["f3"].max()
vmid_global = df["f3"].median()  # 中央値

print(f"全体の値の範囲: {vmin_global:.4f} - {vmax_global:.4f}")
print(f"中央値: {vmid_global:.4f}")

# 共通のカラースケール
norm_global = colors.Normalize(vmin=vmin_global, vmax=vmax_global, clip=True)
cmap = plt.get_cmap(SELECTED_CMAP)

# ========== 論文用: 2行3列配置（共通カラースケール + 出土地点） ==========
fig = plt.figure(figsize=FIGSIZE_PAPER)

# GridSpecで上段3つ、下段2つ（中央寄せ）のレイアウトを作成
gs = GridSpec(2, 6, figure=fig, hspace=0.3, wspace=0.4)

# 軸の配置
axes = []
axes.append(fig.add_subplot(gs[0, 0:2]))  # 上段左
axes.append(fig.add_subplot(gs[0, 2:4]))  # 上段中央
axes.append(fig.add_subplot(gs[0, 4:6]))  # 上段右
axes.append(fig.add_subplot(gs[1, 1:3]))  # 下段左寄り
axes.append(fig.add_subplot(gs[1, 3:5]))  # 下段右寄り

for idx, (ax, jomon) in enumerate(zip(axes[:n_jomon], jomon_list)):
    sub = df[df["Jomon"] == jomon]
    
    # 共通スケールで色設定
    color_dict = {
        row.pref_code: colors.rgb2hex(cmap(norm_global(row.f3)))
        for row in sub.itertuples()
    }
    img = picture(color_dict)
    
    # 地図をプロット
    ax.imshow(img)
    ax.axis("off")
    
    # サンプル出土地点をプロット
    if jomon in SITE_LOCATIONS:
        site = SITE_LOCATIONS[jomon]
        # 画像のサイズを取得
        img_height, img_width = img.shape[:2]
        # 相対座標を絶対座標に変換
        x_pos = site["img_x"] * img_width
        y_pos = site["img_y"] * img_height
        
        # 星マーカーをプロット（黒い縁取り付きの黄色い星）
        ax.plot(x_pos, y_pos, marker='o', markersize=10, 
                color='yellow', markeredgecolor='black', 
                markeredgewidth=1.5, zorder=10)
        
        # オプション：地点名を追加（小さめのフォント）
        # ax.text(x_pos, y_pos-15, site["name"], 
        #         fontsize=8, ha='center', va='bottom',
        #         bbox=dict(boxstyle='round,pad=0.3', 
        #                  facecolor='white', alpha=0.7))
    
    # 各集団の統計情報をタイトルに追加
    mean_val = sub["f3"].mean()
    min_val = sub["f3"].min()
    max_val = sub["f3"].max()
    ax.set_title(f"{jomon}\n(mean={mean_val:.4f})", 
                 fontsize=12, fontweight='bold', pad=10)
    
    print(f"✓ {jomon}: range={min_val:.4f}-{max_val:.4f}, mean={mean_val:.4f}")

# 全体で共通のカラーバー（右側に配置）
cbar_ax = fig.add_axes([0.92, 0.25, 0.02, 0.5])
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm_global)
sm.set_array([])
cbar = fig.colorbar(sm, cax=cbar_ax)
cbar.set_label("f3", rotation=0, labelpad=15, fontsize=12)
cbar.ax.tick_params(labelsize=10)

# カラーバーの値を小数表示でフォーマット
import matplotlib.ticker as ticker
cbar.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))

# 中央値に線を追加（オプション）
cbar.ax.axhline(y=vmid_global, color='black', linestyle='--', linewidth=0.5, alpha=0.5)

# 凡例を追加（星マーカーの説明）
from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], marker='o', color='w', 
                          markerfacecolor='yellow', markeredgecolor='black',
                          markersize=12, label='Sample site')]
fig.legend(handles=legend_elements, loc='lower right', 
          bbox_to_anchor=(0.9, 0.05), fontsize=10)

# 全体のタイトル
fig.suptitle("Outgroup f3(Jomon, Modern Japanese; Mbuti)", 
             fontsize=16, fontweight='bold', y=0.98)

# レイアウト調整
fig.subplots_adjust(right=0.9)

# 保存
paper_png = os.path.join(OUTDIR, f"Jomon_f3_prefecture_with_sites_{SELECTED_CMAP}.png")
fig.savefig(paper_png, dpi=300, bbox_inches='tight')
plt.close(fig)

print(f"\n✓ 出土地点付き共通スケール版出力: {paper_png}")

# ========== 比較用: 個別スケール版（出土地点付き）も同時に生成 ==========
SAVE_INDIVIDUAL_SCALE = True

if SAVE_INDIVIDUAL_SCALE:
    fig2 = plt.figure(figsize=FIGSIZE_PAPER)
    gs2 = GridSpec(2, 6, figure=fig2, hspace=0.3, wspace=0.5)
    
    axes2 = []
    axes2.append(fig2.add_subplot(gs2[0, 0:2]))
    axes2.append(fig2.add_subplot(gs2[0, 2:4]))
    axes2.append(fig2.add_subplot(gs2[0, 4:6]))
    axes2.append(fig2.add_subplot(gs2[1, 1:3]))
    axes2.append(fig2.add_subplot(gs2[1, 3:5]))
    
    for idx, (ax, jomon) in enumerate(zip(axes2[:n_jomon], jomon_list)):
        sub = df[df["Jomon"] == jomon]
        
        # 個別スケール
        vmin_local = sub["f3"].min()
        vmax_local = sub["f3"].max()
        norm_local = colors.Normalize(vmin=vmin_local, vmax=vmax_local, clip=True)
        
        color_dict = {
            row.pref_code: colors.rgb2hex(cmap(norm_local(row.f3)))
            for row in sub.itertuples()
        }
        img = picture(color_dict)
        
        ax.imshow(img)
        ax.axis("off")
        ax.set_title(jomon, fontsize=14, fontweight='bold', pad=10)
        
        # サンプル出土地点をプロット
        if jomon in SITE_LOCATIONS:
            site = SITE_LOCATIONS[jomon]
            img_height, img_width = img.shape[:2]
            x_pos = site["img_x"] * img_width
            y_pos = site["img_y"] * img_height
            
            ax.plot(x_pos, y_pos, marker='*', markersize=20, 
                    color='yellow', markeredgecolor='black', 
                    markeredgewidth=1.5, zorder=10)
        
        # 個別カラーバー
        from mpl_toolkits.axes_grid1 import make_axes_locatable
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="8%", pad=0.05)
        
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm_local)
        sm.set_array([])
        cbar = fig2.colorbar(sm, cax=cax)
        cbar.ax.tick_params(labelsize=9)
        cbar.set_label("f3", rotation=0, labelpad=15, fontsize=10)
        
        # 小数表示
        cbar.ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
    
    # 凡例を追加
    legend_elements = [Line2D([0], [0], marker='*', color='w', 
                              markerfacecolor='yellow', markeredgecolor='black',
                              markersize=12, label='Sample site')]
    fig2.legend(handles=legend_elements, loc='lower right', 
               bbox_to_anchor=(0.9, 0.05), fontsize=10)
    
    fig2.suptitle("Outgroup f3(Jomon, Modern Japanese; Mbuti) - Individual Scales", 
                  fontsize=16, fontweight='bold', y=0.98)
    
    individual_png = os.path.join(OUTDIR, "Jomon_f3_prefecture_individual_with_sites.png")
    fig2.savefig(individual_png, dpi=300, bbox_inches='tight')
    plt.close(fig2)
    print(f"✓ 出土地点付き個別スケール版も出力: {individual_png}")

print("\n== サンプル出土地点 ==")
for jomon in jomon_order:
    if jomon in SITE_LOCATIONS:
        site = SITE_LOCATIONS[jomon]
        print(f"{jomon}: {site['name']}")

print("\n完了しました。")