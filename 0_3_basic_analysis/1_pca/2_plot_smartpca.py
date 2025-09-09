import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

EVEC_PATH = "/home/mkato/hdd_data/0_3_basic_analysis/1_pca/pca_result.targetpops.evec"
OUTPUT_PATH_PC1_PC2 = "/home/mkato/mkato-jomon/0_3_basic_analysis/1_pca/pca_plot_PC1_PC2.png"
OUTPUT_PATH_PC1_PC3 = "/home/mkato/mkato-jomon/0_3_basic_analysis/1_pca/pca_plot_PC1_PC3.png"

CLASS_ORDER = ["Control", "Ancients", "Case"]  # ← 描画順を制御
CLASS_CMAP = {
    "Case": "twilight_shifted",
    "Ancients": "rainbow",
    "Control": "nipy_spectral",
}

# Case集団用の個別色指定
CASE_COLORS = {
    "Todoroki": "#12E655",     # 赤
    "Chidorigakubo": "#4ECDC4",         # ターコイズ
    "Mitsusawa": "#0E162E",       # 青
    "Funadomari": "#F317D6", 
    "Iyai": "#FF6347",  # トマト
    }

CLASS_MARKERS = {
    "Case": ["*","*","*","*", "*"],
    "Ancients": ["s", "o", "v", "^", "<", ">", "p", "h"],
    "Control": ["s", "o", "^", "<", ">", "p", "h"],
}

def assign_shapes(df):
    pop2shape = {}
    for cls in CLASS_ORDER:
        pops = sorted(df[df["class"] == cls]["pop"].unique())
        shapes = CLASS_MARKERS[cls]
        for i, pop in enumerate(pops):
            pop2shape[pop] = shapes[i % len(shapes)]  # 循環割り当て
    return pop2shape


def load_evec(path):
    records = []
    with open(path) as fh:
        for ln in fh:
            ln = ln.strip()
            if not ln or ln.startswith("#"):
                continue
            cols = ln.split()
            pop = cols[0].split(":")[0]
            records.append({
                "pop":   pop,
                "PC1":   float(cols[1]),
                "PC2":   float(cols[2]),
                "PC3":   float(cols[3]),
                "class": cols[-1],
            })
    return pd.DataFrame(records)


def build_shape_color_maps(df):
    pop2shape, pop2color = {}, {}
    for cls in CLASS_ORDER:
        pops = sorted(df.loc[df["class"] == cls, "pop"].unique())
        shapes = CLASS_MARKERS[cls]
        
        if cls == "Case":
            # Case集団には個別色を指定
            for i, pop in enumerate(pops):
                pop2shape[pop] = shapes[i % len(shapes)]
                pop2color[pop] = CASE_COLORS.get(pop, "#000000")  # デフォルト色は黒
        else:
            # それ以外はカラーマップを使用
            cmap = plt.cm.get_cmap(CLASS_CMAP[cls], max(len(pops), 3))
            color_idxs = np.linspace(0.2, 0.9, len(pops))
            for i, pop in enumerate(pops):
                pop2shape[pop] = shapes[i % len(shapes)]
                pop2color[pop] = cmap(color_idxs[i])
    return pop2shape, pop2color

def plot(df, out_png, pc_x="PC1", pc_y="PC2", figsize=(10, 8)):
    fig, ax = plt.subplots(figsize=figsize)
    pop2shape, pop2color = build_shape_color_maps(df)

    # legend order: maintain CLASS_ORDER with alphabetical populations
    
    for cls in CLASS_ORDER:
        cls_df = df[df["class"] == cls]
        if cls == "Control":
            cls_alpha = 0.9
            cls_face = None
        elif cls == "Ancients":
            cls_alpha = 0.6
            cls_face = "none"
        else:
            cls_alpha = 0.9
            cls_face = None

        pops = sorted(cls_df["pop"].unique())
        for pop in pops:
            sub = cls_df[cls_df["pop"] == pop]
            facecolors = cls_face if cls_face is not None else pop2color[pop]
            ax.scatter(sub[pc_x], sub[pc_y],
                    marker=pop2shape[pop],
                    c=pop2color[pop],
                    facecolors=facecolors,
                    edgecolors="k",
                    linewidths=0.4,
                    s=55,
                    alpha=cls_alpha,
                    label=pop)

    ax.set_xlabel(pc_x)
    ax.set_ylabel(pc_y)
    #ax.set_title(f"PCA: {pc_x} vs {pc_y}")

    # 凡例ハンドルとラベルを取得
    handles, labels = ax.get_legend_handles_labels()

    # 各 population が属するクラスを引くための辞書
    pop2class = dict(zip(df["pop"], df["class"]))

    # 優先度テーブル：小さいほど先に並ぶ
    class_priority = {"Case": 0, "Ancients": 1, "Control": 2}

    # (ラベル, ハンドル) を希望順にソート
    sorted_pairs = sorted(
        zip(labels, handles),
        key=lambda x: (class_priority[pop2class[x[0]]], x[0])  # クラス優先 → アルファベット
    )

    # ラベル重複の除去（念のため）
    seen = set()
    uniq_handles, uniq_labels = [], []
    for lbl, hdl in sorted_pairs:
        if lbl not in seen:
            seen.add(lbl)
            uniq_handles.append(hdl)
            uniq_labels.append(lbl)

    # 凡例を描画 - クラス区切りをつける
    legend_handles = []
    legend_labels = []
    
    for i, (label, handle) in enumerate(zip(uniq_labels, uniq_handles)):
        # 前の要素のクラスと現在のクラスが異なる場合、空行を追加
        if i > 0:
            prev_class = pop2class[uniq_labels[i-1]]
            curr_class = pop2class[label]
            if prev_class != curr_class:
                # 透明なダミーハンドル追加
                legend_handles.append(plt.Line2D([0], [0], color='white', alpha=0))
                legend_labels.append('')
        
        legend_handles.append(handle)
        legend_labels.append(label)

    ax.legend(
        legend_handles,
        legend_labels,
        title="Population",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        frameon=False,
    )

    plt.tight_layout()
    fig.savefig(out_png, dpi=300, bbox_inches="tight")
    plt.show()

# Execute
df = load_evec(EVEC_PATH)
plot(df, OUTPUT_PATH_PC1_PC2, "PC1", "PC2")
plot(df, OUTPUT_PATH_PC1_PC3, "PC1", "PC3")