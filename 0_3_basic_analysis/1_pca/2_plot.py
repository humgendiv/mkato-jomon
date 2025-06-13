#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_pca_evec_improved.py

SmartPCA の .evec を読み込んで
・PC1 vs PC2 を散布図にプロット
・色で Population、形状で Class (Case/Control) を表現
・凡例を見切れないようにレイアウト調整
"""

import argparse
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

def main():
    parser = argparse.ArgumentParser(description="Improved PCA plot from SmartPCA .evec")
    parser.add_argument('-i', '--input', default='/home/mkato/hdd_data/0_3_basic_analysis/1_pca/pca_result.targetpops.evec',
                        help="入力 .evec ファイルパス")
    parser.add_argument('-o', '--output', default='pca_improved.png',
                        help="出力画像 (PNG)")
    args = parser.parse_args()

    # ---- データ読み込み ----
    df = pd.read_csv(
        args.input,
        sep=r'\s+',
        comment='#',
        header=None,
        engine='python'
    )
    ncol = df.shape[1]
    cols = ['SampleID'] + [f'PC{i}' for i in range(1, ncol-1)] + ['Class']
    df.columns = cols

    # pop prefix を抽出
    df['pop'] = df['SampleID'].str.split(pat=':', n=1).str[0]

    # 色マップ
    pops = sorted(df['pop'].unique())
    cmap = plt.get_cmap('tab20')
    color_map = {pop: cmap(i % cmap.N) for i, pop in enumerate(pops)}

    # Class → マーカー形状マップ
    marker_map = {'Case': '*', 'Control': 'o'}
    df['marker'] = df['Class'].map(marker_map).fillna('x')

    # ---- プロット ----
    fig, ax = plt.subplots(figsize=(12, 8))
    for pop, sub in df.groupby('pop'):
        for cls, cls_df in sub.groupby('Class'):
            mk = marker_map.get(cls, 'x')
            ax.scatter(
                cls_df['PC1'], cls_df['PC2'],
                s=100 if cls == 'Case' else 50,        # Case を大きめに
                marker=mk,
                c=[color_map[pop]] * len(cls_df),
                edgecolor='black' if cls == 'Case' else 'none',
                linewidth=0.6,
                alpha=0.9
            )

    # 軸ラベル・タイトル
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_title('PCA (PC1 vs PC2)')

    # グリッドを薄く描画
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.4)

    # ---- 凡例 ----
    # Population（色）
    pop_handles = [
        mlines.Line2D([], [], color=color_map[pop], marker='o', linestyle='None',
                      markersize=6, label=pop)
        for pop in pops
    ]
    legend1 = ax.legend(handles=pop_handles,
                        title='Population',
                        fontsize=6, title_fontsize=8,
                        loc='upper left',
                        bbox_to_anchor=(1.02, 1))
    ax.add_artist(legend1)

    # Class（形状）
    class_handles = [
        mlines.Line2D([], [], color='black', marker=marker_map['Case'],
                      linestyle='None', markersize=10, label='Case'),
        mlines.Line2D([], [], color='gray', marker=marker_map['Control'],
                      linestyle='None', markersize=6, label='Control'),
    ]
    ax.legend(handles=class_handles,
              title='Class',
              fontsize=8, title_fontsize=8,
              loc='upper left',
              bbox_to_anchor=(1.02, 0.6))

    # 右側に凡例を収める余白を確保
    plt.subplots_adjust(right=0.75)
    plt.tight_layout()
    fig.savefig(args.output, dpi=300)
    print(f"Saved improved plot to {args.output}")

if __name__ == '__main__':
    main()
