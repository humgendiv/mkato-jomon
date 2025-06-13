import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

EVEC_PATH = "/home/mkato/hdd_data/0_3_basic_analysis/1_pca/pca_result.targetpops.evec"
OUTPUT_PATH = "/home/mkato/mkato-jomon/0_3_basic_analysis/1_pca/pca_plot.png"

CLASS_ORDER = ["Control", "Ancients", "Case"]  # ← 描画順を制御
CLASS_CMAP = {
    "Case": "gnuplot",
    "Ancients": "rainbow",
    "Control": "nipy_spectral",
}

CLASS_MARKERS = {
    "Case": ["*","d","X","8"],
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
                "class": cols[-1],
            })
    return pd.DataFrame(records)


def build_shape_color_maps(df):
    pop2shape, pop2color = {}, {}
    for cls in CLASS_ORDER:
        pops = sorted(df.loc[df["class"] == cls, "pop"].unique())
        cmap = plt.cm.get_cmap(CLASS_CMAP[cls], max(len(pops), 3))
        color_idxs = np.linspace(0.2, 0.9, len(pops))
        shapes = CLASS_MARKERS[cls]
        for i, pop in enumerate(pops):
            pop2shape[pop] = shapes[i % len(shapes)]
            pop2color[pop] = cmap(color_idxs[i])
    return pop2shape, pop2color

def plot(df, out_png, figsize=(10, 8)):
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
            ax.scatter(sub["PC1"], sub["PC2"],
                    marker=pop2shape[pop],
                    c=pop2color[pop],
                    facecolors=facecolors,
                    edgecolors="k",
                    linewidths=0.4,
                    s=55,
                    alpha=cls_alpha,
                    label=pop)

    ax.set_xlabel("PC1")
    ax.set_ylabel("PC2")
    #ax.set_title("PCA: PC1 vs PC2")

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

    # 凡例を描画
    ax.legend(
        uniq_handles,
        uniq_labels,
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
plot(df, OUTPUT_PATH)