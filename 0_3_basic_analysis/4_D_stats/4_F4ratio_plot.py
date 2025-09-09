#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import os

# ファイルパスの設定
log_file = "/home/mkato/mkato-jomon/0_3_basic_analysis/4_D_stats/qpF4ratio.log"
output_dir = "/home/mkato/mkato-jomon/0_3_basic_analysis/4_D_stats/plots"

# 出力ディレクトリが存在しない場合は作成
os.makedirs(output_dir, exist_ok=True)

# ログファイルの読み込みと解析
results = []
with open(log_file, 'r') as f:
    for line in f:
        if line.strip().startswith('result:'):
            # 結果行の解析
            parts = line.strip().split()
            # フォーマット: result: pop1 pop2 pop3 pop4 : pop1 pop2 pop5 pop4 alpha std_err Z_score
            pop3 = parts[3]
            pop4 = parts[4]
            pop5 = parts[8]
            alpha = float(parts[10])
            std_err = float(parts[11])
            
            results.append({
                'pop3': pop3,
                'pop4': pop4,
                'pop5': pop5,
                'alpha': alpha,
                'std_err': std_err
            })

# データフレームに変換
df = pd.DataFrame(results)

# pop5ごとにグループ化（Korean vs Han）
korean_data = df[df['pop5'] == 'Korean'].copy()
han_data = df[df['pop5'] == 'Han'].copy()

# pop4の順序を設定
pop4_order = ['Iyai', 'Todoroki', 'Funadomari', 'Chidorigakubo', 'Mitsusawa']

# カラーパレット（画像を参考に、異なる色合いを使用）
jomon_color = '#FF6B6B'  # 赤系
korean_color = '#4ECDC4'  # 青緑系

# Figure 1: Korean comparison (本文用)
fig1, ax1 = plt.subplots(1, 1, figsize=(8, 6))

for i, pop4 in enumerate(pop4_order):
    if pop4 in korean_data['pop4'].values:
        data = korean_data[korean_data['pop4'] == pop4]
        alpha = data['alpha'].values[0]
        std_err = data['std_err'].values[0]
        
        # 積み上げ棒グラフ（1-alphaが縄文成分）
        ax1.bar(i, 1-alpha, color=jomon_color, label='Jomon related ancestry' if i == 0 else '')
        ax1.bar(i, alpha, bottom=1-alpha, color=korean_color, label='Korean related ancestry' if i == 0 else '')
        
        # エラーバー（1-alphaの位置に配置）
        ax1.errorbar(i, 1-alpha, yerr=std_err, fmt='none', color='black', capsize=5)

ax1.set_ylabel('ancestry proportion', fontsize=12)
ax1.set_ylim(0, 1.0)
ax1.set_xticks(range(len(pop4_order)))
ax1.set_xticklabels([f'{pop}_Type' if pop == 'Dogijima' else pop for pop in pop4_order], rotation=45, ha='right')
ax1.set_title('f4 ratio test', fontsize=14)
ax1.legend(loc='lower center', bbox_to_anchor=(0.5, -0.35), ncol=2)

# レイアウトの調整
plt.tight_layout()

# Korean比較のグラフを保存（本文用）
output_path_korean = os.path.join(output_dir, 'f4ratio_korean.png')
plt.savefig(output_path_korean, dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(output_dir, 'f4ratio_korean.pdf'), bbox_inches='tight')
plt.close(fig1)

print(f"Korean比較グラフを保存しました: {output_path_korean}")

# Figure 2: Han comparison (supplementary用)
fig2, ax2 = plt.subplots(1, 1, figsize=(8, 6))

for i, pop4 in enumerate(pop4_order):
    if pop4 in han_data['pop4'].values:
        data = han_data[han_data['pop4'] == pop4]
        alpha = data['alpha'].values[0]
        std_err = data['std_err'].values[0]
        
        # 積み上げ棒グラフ（1-alphaが縄文成分）
        ax2.bar(i, 1-alpha, color=jomon_color, label='Jomon related ancestry' if i == 0 else '')
        ax2.bar(i, alpha, bottom=1-alpha, color=korean_color, label='Han related ancestry' if i == 0 else '')
        
        # エラーバー（1-alphaの位置に配置）
        ax2.errorbar(i, 1-alpha, yerr=std_err, fmt='none', color='black', capsize=5)

ax2.set_ylabel('ancestry proportion', fontsize=12)
ax2.set_ylim(0, 1.0)
ax2.set_xticks(range(len(pop4_order)))
ax2.set_xticklabels([f'{pop}_Type' if pop == 'Dogijima' else pop for pop in pop4_order], rotation=45, ha='right')
ax2.set_title('f4 ratio test', fontsize=14)
ax2.legend(loc='lower center', bbox_to_anchor=(0.5, -0.35), ncol=2)

# レイアウトの調整
plt.tight_layout()

# Han比較のグラフを保存（supplementary用）
output_path_han = os.path.join(output_dir, 'f4ratio_han_supplementary.png')
plt.savefig(output_path_han, dpi=300, bbox_inches='tight')
plt.savefig(os.path.join(output_dir, 'f4ratio_han_supplementary.pdf'), bbox_inches='tight')
plt.close(fig2)

print(f"Han比較グラフを保存しました: {output_path_han}")

# 結果のサマリーを表示
print("\n=== f4 ratio 結果サマリー ===")
print("\nKorean comparison:")
for _, row in korean_data.iterrows():
    print(f"{row['pop4']}: Jomon ancestry = {1-row['alpha']:.3f} ± {row['std_err']:.3f}")

print("\nHan comparison:")
for _, row in han_data.iterrows():
    print(f"{row['pop4']}: Jomon ancestry = {1-row['alpha']:.3f} ± {row['std_err']:.3f}")