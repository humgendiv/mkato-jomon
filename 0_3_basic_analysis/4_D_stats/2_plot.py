import pandas as pd
import matplotlib.pyplot as plt
import os

def parse_qpdstat_log(log_path):
    results = []
    with open(log_path, 'r') as f:
        for line in f:
            if line.startswith("result:"):
                parts = line.strip().split()
                outgroup = parts[1]
                continental = parts[2]
                pop1 = parts[3]
                pop2 = parts[4]
                f4 = float(parts[5])
                z = float(parts[6])
                results.append([continental, pop1, pop2, f4, z])
    df = pd.DataFrame(results, columns=["Continental", "Pop1", "Pop2", "f4", "Z"])
    return df

def plot_f4_with_z_filter(df, continental, output_dir, z_threshold=3):
    subset = df[df["Continental"] == continental].copy()
    subset["Comparison"] = "( "+subset["Pop1"] + ", " + subset["Pop2"]+ ")"
    grouped = subset.groupby("Comparison").agg({"f4": "mean", "Z": "mean"}).reset_index()
    grouped["SE"] = abs(grouped["f4"] / grouped["Z"].replace(0, 1))  # avoid division by zero
    grouped["Alpha"] = grouped["Z"].abs().apply(lambda z: 1.0 if z >= z_threshold else 0.3)
    grouped.sort_values("f4", ascending=True, inplace=True)

    plt.figure(figsize=(10, len(grouped) * 0.35))
    for _, row in grouped.iterrows():
        plt.errorbar(row["f4"], row["Comparison"], xerr=row["SE"], fmt='s',
                     color='black', ecolor='black', alpha=row["Alpha"], capsize=3)

    plt.xlabel(f"f4(Mbuti, {continental}; X, Y)")
    plt.title(f"f4-like Plot (Z ≥ {z_threshold} highlighted): {continental}")
    plt.grid(True, axis='x', linestyle='--', alpha=0.4)
    plt.tight_layout()

    # 保存
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, f"f4_plot_{continental}.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[Saved] {out_path}")

# === 実行 ===
# ログファイルのパス
log_file = "./qpDstat.log"  # 例: "./qpDstat.log"
output_dir = "/home/mkato/mkato-jomon/0_3_basic_analysis/4_D_stats/plots"   # 出力ディレクトリ

# 読み込み
df = parse_qpdstat_log(log_file)

# 対象とするContinental集団
target_continentals = ["Han", "Japanese", "Korean"]

# プロットと保存
for pop in target_continentals:
    plot_f4_with_z_filter(df, pop, output_dir, z_threshold=3)
