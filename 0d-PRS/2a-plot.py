import pandas as pd
import matplotlib.pyplot as plt

def plot_PRS_diff(threshold, sort_by="mean"):
    """
    PRSの差を現代日本人と比較してプロット。
    ソート方法は "mean" または "variance" を選択可能。
    
    threshold: p値の閾値
    sort_by: "mean" で平均値に基づいてソート、"variance" で分散に基づいてソート
    """
    
    # データの読み込み
    data = pd.read_csv(f"/home/mkato/hdd_data/2-2-polygenic/PRS_scores/PRS_scores_p{threshold}.txt", sep="\t", comment="#", index_col=0)

    # 現代日本人の値を引いて差分を計算
    jomon_diff = data.iloc[:-1, :] - data.iloc[-1, :]

    # 個体名をアンダーバーより前の部分のみに変更
    jomon_diff.index = [idx.split("_")[-1] for idx in jomon_diff.index]

    # 4個体の統計量を計算し、ソート基準を選択
    if sort_by == "mean":
        stat_diff = jomon_diff.mean(axis=0)
    elif sort_by == "variance":
        stat_diff = jomon_diff.var(axis=0)
    else:
        raise ValueError('sort_by must be either "mean" or "variance"')

    # ソート順を決定
    sorted_traits = stat_diff.sort_values(ascending=True).index

    # 図の作成
    fig, ax = plt.subplots(figsize=(10, 20))

    # 各縄文人個体をプロット
    for individual in jomon_diff.index:
        valid_traits = jomon_diff.loc[individual, sorted_traits].dropna()  # 欠損値を除外
        ax.scatter(jomon_diff.loc[individual, sorted_traits], range(len(sorted_traits)), label=individual, s=100, alpha=0.8)

    # 縦軸の設定
    ax.set_yticks(range(len(sorted_traits)))
    ax.set_yticklabels(sorted_traits)

    # 軸ラベルとタイトルの設定
    ax.set_xlabel("Difference from Modern Japanese")
    ax.set_ylabel("Traits")
    ax.set_title(f"Polygenic Risk Score Differences between Jomon and Modern Japanese (GWAS P-value threshold = {threshold}, sorted by {sort_by})")

    # 0のラインを赤く太めに設定
    ax.axvline(x=0, color='red', linewidth=2)

    # 凡例の設定
    ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")

    # グリッド線の追加
    ax.grid(axis="x", linestyle="--", alpha=0.7)

    # 図の保存と表示
    plt.tight_layout()
    plt.savefig(f"PRS_diff_Jomon_vs_Japanese_p{threshold}_sorted_by_{sort_by}.png", dpi=300, bbox_inches="tight")

# 実行
#plot_PRS_diff(0.01, sort_by="mean")     # 平均値でソート
plot_PRS_diff(0.01, sort_by="variance") # 分散でソート
