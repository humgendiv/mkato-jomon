#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_japan_map_with_sites.py
論文Fig.1用: 日本地図に縄文遺跡の位置をプロット
依存: cartopy, matplotlib, numpy
インストール: conda install -c conda-forge cartopy
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import numpy as np
import os

# ---------- 設定 ----------
OUTDIR = "/home/mkato/mkato-jomon/0_4_analysis/3_prefecture/maps"
DPI = 300  # 論文用高解像度

# 遺跡の位置情報
SITES = {
    'Funadomari': {
        'lon': 141.05,
        'lat': 45.30,
        'name_jp': '船泊遺跡',
        'location': 'Rebun Island, Hokkaido',
        'age': 'Late Jomon (3,800-3,500 BP)'
    },
    'Chidorigakubo': {
        'lon': 139.70,
        'lat': 35.58,
        'name_jp': '千鳥久保遺跡',
        'location': 'Ota, Tokyo',
        'age': 'Middle Jomon (4,000-3,000 BP)'
    },
    'Mitsusawa': {
        'lon': 139.62,
        'lat': 35.47,
        'name_jp': '三ツ沢遺跡',
        'location': 'Yokohama, Kanagawa',
        'age': 'Middle Jomon (4,500-3,500 BP)'
    },

    'Todoroki': {
        'lon': 130.66,
        'lat': 32.69,
        'name_jp': '轟貝塚',
        'location': 'Uto, Kumamoto',
        'age': 'Early Jomon (7,000-5,500 BP)'
    },
        'Iyai': {
        'lon': 138.65,
        'lat': 36.56,
        'name_jp': '居家以遺跡',
        'location': 'Naganohara, Gunma',
        'age': 'Initial Jomon (5,000-4,000 BP)'
    },
}

# 時代順（古い順）にソート
SITE_ORDER = ['Iyai','Todoroki', 'Mitsusawa', 'Chidorigakubo', 'Funadomari']

# ---------- メイン処理 ----------
os.makedirs(OUTDIR, exist_ok=True)

# ========== Figure 1: シンプルな位置図 ==========
fig = plt.figure(figsize=(8, 10))
ax = plt.axes(projection=ccrs.PlateCarree())

# 日本全体が入る範囲を設定
ax.set_extent([128, 146, 30, 46], ccrs.PlateCarree())

# 地図要素を追加
# 陸地（薄いグレー）
ax.add_feature(cfeature.LAND, facecolor='#f0f0f0', edgecolor='none')
# 海（薄い青）
ax.add_feature(cfeature.OCEAN, facecolor='#e6f2ff')
# 海岸線（細い黒線）
ax.add_feature(cfeature.COASTLINE, linewidth=0.5, color='#333333')

# グリッド線を追加（薄いグレー）
gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', 
                  alpha=0.3, linestyle='--')
gl.top_labels = False
gl.right_labels = False
gl.xformatter = LongitudeFormatter()
gl.yformatter = LatitudeFormatter()
gl.xlabel_style = {'size': 9}
gl.ylabel_style = {'size': 9}

# 遺跡位置をプロット（時代順に番号付け）
for idx, site_key in enumerate(SITE_ORDER, 1):
    site = SITES[site_key]
    lon, lat = site['lon'], site['lat']
    
    # マーカーをプロット（赤い円）
    ax.plot(lon, lat, 'o', color='red', markersize=10, 
            markeredgecolor='darkred', markeredgewidth=1.5,
            transform=ccrs.PlateCarree(), zorder=5)
    
    # 番号を追加
    ax.text(lon, lat, str(idx), color='white', fontsize=8, 
            fontweight='bold', ha='center', va='center',
            transform=ccrs.PlateCarree(), zorder=6)
    
    # サイト名を追加（位置を調整）
    # 位置調整用のオフセット
    offsets = {
        'Funadomari': (0.5, 0),
        'Chidorigakubo': (0.7, 0),
        'Mitsusawa': (0.7, -0.3),
        'Iyai': (0.7, 0),
        'Todoroki': (-1.0, 0)
    }
    
    offset_x, offset_y = offsets.get(site_key, (0.5, 0))
    ax.text(lon + offset_x, lat + offset_y, site_key, 
            fontsize=9, ha='left', va='center',
            transform=ccrs.PlateCarree(),
            bbox=dict(boxstyle='round,pad=0.2', 
                     facecolor='white', alpha=0.8, edgecolor='none'))

# スケールバーを追加（簡易版）
# 左下に200kmスケール
scale_lon = 129
scale_lat = 31
scale_length = 200  # km
# 緯度1度 ≈ 111 km として概算
scale_deg = scale_length / 111

ax.plot([scale_lon, scale_lon + scale_deg], [scale_lat, scale_lat], 
        'k-', linewidth=2, transform=ccrs.PlateCarree())
ax.text(scale_lon + scale_deg/2, scale_lat - 0.3, '200 km', 
        ha='center', fontsize=9, transform=ccrs.PlateCarree())

# 北矢印を追加
ax.text(144.5, 44.5, '↑\nN', ha='center', va='center', 
        fontsize=12, fontweight='bold', transform=ccrs.PlateCarree())

# タイトル
#ax.set_title('Jomon Archaeological Sites', fontsize=14, fontweight='bold', pad=20)

# 保存
output_path = os.path.join(OUTDIR, 'Fig1_japan_map_sites_simple.png')
plt.tight_layout()
plt.savefig(output_path, dpi=DPI, bbox_inches='tight', facecolor='white')
plt.close()

print(f"✓ シンプル版を出力: {output_path}")

# ========== Figure 1b: 詳細情報付きバージョン ==========
fig = plt.figure(figsize=(10, 12))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.set_extent([128, 146, 30, 46], ccrs.PlateCarree())

# 地図要素
ax.add_feature(cfeature.LAND, facecolor='#f0f0f0', edgecolor='none')
ax.add_feature(cfeature.OCEAN, facecolor='#e6f2ff')
ax.add_feature(cfeature.COASTLINE, linewidth=0.5, color='#333333')
# 県境を薄く追加（オプション）
# ax.add_feature(cfeature.BORDERS, linewidth=0.3, alpha=0.3)

# グリッド
gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', 
                  alpha=0.3, linestyle='--')
gl.top_labels = False
gl.right_labels = False
gl.xformatter = LongitudeFormatter()
gl.yformatter = LatitudeFormatter()
gl.xlabel_style = {'size': 9}
gl.ylabel_style = {'size': 9}

# カラーマップ（時代順に色を変える）
colors_time = plt.cm.RdYlBu_r(np.linspace(0.2, 0.8, len(SITE_ORDER)))

# 遺跡をプロット
for idx, (site_key, color) in enumerate(zip(SITE_ORDER, colors_time), 1):
    site = SITES[site_key]
    lon, lat = site['lon'], site['lat']
    
    # マーカー（時代によって色を変える）
    ax.plot(lon, lat, 'o', color=color, markersize=12, 
            markeredgecolor='black', markeredgewidth=1.5,
            transform=ccrs.PlateCarree(), zorder=5)
    
    # 番号
    ax.text(lon, lat, str(idx), color='white', fontsize=9, 
            fontweight='bold', ha='center', va='center',
            transform=ccrs.PlateCarree(), zorder=6)

# 凡例を作成
legend_elements = []
for idx, site_key in enumerate(SITE_ORDER, 1):
    site = SITES[site_key]
    label = f"{idx}. {site_key}\n   {site['age']}"
    color = colors_time[idx-1]
    from matplotlib.lines import Line2D
    element = Line2D([0], [0], marker='o', color='w', 
                    markerfacecolor=color, markeredgecolor='black',
                    markersize=10, label=label)
    legend_elements.append(element)

ax.legend(handles=legend_elements, loc='upper left', 
         bbox_to_anchor=(0.02, 0.98), fontsize=8,
         title='Archaeological Sites', title_fontsize=9,
         frameon=True, fancybox=True, framealpha=0.9)

# スケールバー
scale_lon = 129
scale_lat = 31
scale_length = 200
scale_deg = scale_length / 111

ax.plot([scale_lon, scale_lon + scale_deg], [scale_lat, scale_lat], 
        'k-', linewidth=2, transform=ccrs.PlateCarree())
ax.plot([scale_lon, scale_lon], [scale_lat - 0.05, scale_lat + 0.05], 
        'k-', linewidth=2, transform=ccrs.PlateCarree())
ax.plot([scale_lon + scale_deg, scale_lon + scale_deg], 
        [scale_lat - 0.05, scale_lat + 0.05], 
        'k-', linewidth=2, transform=ccrs.PlateCarree())
ax.text(scale_lon + scale_deg/2, scale_lat - 0.3, '200 km', 
        ha='center', fontsize=9, transform=ccrs.PlateCarree())

# 北矢印
ax.annotate('', xy=(144.5, 45), xytext=(144.5, 44),
            arrowprops=dict(arrowstyle='->', lw=2, color='black'),
            transform=ccrs.PlateCarree())
ax.text(144.5, 44.5, 'N', ha='center', va='center', 
        fontsize=12, fontweight='bold', transform=ccrs.PlateCarree())

# タイトル
#ax.set_title('Location of Jomon Archaeological Sites', 
#            fontsize=14, fontweight='bold', pad=20)

# 小さいインセット地図（日本の位置を示す）
ax_inset = fig.add_axes([0.7, 0.15, 0.25, 0.25], 
                        projection=ccrs.PlateCarree())
ax_inset.set_extent([120, 155, 20, 50], ccrs.PlateCarree())
ax_inset.add_feature(cfeature.LAND, facecolor='lightgray')
ax_inset.add_feature(cfeature.OCEAN, facecolor='white')
ax_inset.add_feature(cfeature.COASTLINE, linewidth=0.3)
# 日本を赤い枠で強調
ax_inset.plot([128, 146, 146, 128, 128], [30, 30, 46, 46, 30], 
             'r-', linewidth=1.5, transform=ccrs.PlateCarree())

# 保存
output_path_detailed = os.path.join(OUTDIR, 'Fig1_japan_map_sites_detailed.png')
plt.tight_layout()
plt.savefig(output_path_detailed, dpi=DPI, bbox_inches='tight', facecolor='white')
plt.close()

print(f"✓ 詳細版を出力: {output_path_detailed}")

# ========== サイト情報をテキストファイルに出力 ==========
info_path = os.path.join(OUTDIR, 'site_information.txt')
with open(info_path, 'w', encoding='utf-8') as f:
    f.write("Jomon Archaeological Sites Information\n")
    f.write("=" * 50 + "\n\n")
    
    for idx, site_key in enumerate(SITE_ORDER, 1):
        site = SITES[site_key]
        f.write(f"{idx}. {site_key} ({site['name_jp']})\n")
        f.write(f"   Location: {site['location']}\n")
        f.write(f"   Coordinates: {site['lat']}°N, {site['lon']}°E\n")
        f.write(f"   Period: {site['age']}\n")
        f.write("\n")

print(f"✓ サイト情報を出力: {info_path}")
print("\n完了しました。")