#!/usr/bin/env python3
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Configuration ---
logfile = "./qp3pop.log"
# Define the group order and their matching patterns
group_order = [
    ("Japan_Iyai_Jomon", re.compile("Japan_Iyai_Jomon")),
    ("Japan_Todoroki_Jomon", re.compile("Japan_Todoroki_Jomon")),
    ("Japan_Chidorigakubo_Jomon", re.compile("Japan_Chidorigakubo_Jomon")),
    ("Japan_Mitsusawa_Jomon", re.compile("Japan_Mitsusawa_Jomon")),
    ("Janan_Funadomari_Jomon", re.compile("Janan_Funadomari_Jomon")),
    ("Jomon", re.compile("Jomon")),
    ("Yayoi", re.compile("Yayoi")),
    ("Kofun", re.compile("Kofun")),
    ("Japanese", re.compile("Japanese")),
    ("Korea", re.compile("Korea")),
]

# --- Parse qp3pop log ---
records = []
with open(logfile) as f:
    in_table = False
    for line in f:
        if not in_table:
            # detect start of results table
            if "Source 1" in line and "Target" in line:
                in_table = True
                print("True")
            continue
        line = line.strip()
        if not line or line.startswith("no"):
            continue
        # Expect lines starting with 'result:'
        if not line.startswith("result:"):
            continue
        parts = line.split()
        # parts = ['result:', src1, src2, outgroup, f3, stderr, Z, SNPs]
        if len(parts) < 5:
            continue
        src1, src2, f3_val = parts[1], parts[2], float(parts[4])
        records.append((src1, src2, f3_val))

# Build DataFrame
df = pd.DataFrame(records, columns=["pop1", "pop2", "f3"])
# Determine all populations that match any of the group patterns
all_pops = sorted(
    {p for p in df["pop1"].tolist() + df["pop2"].tolist()
     if any(pat.search(p) for _, pat in group_order)}
)

# Build symmetric matrix for the matched populations
mat = pd.DataFrame(index=all_pops, columns=all_pops, dtype=float)
for _, row in df.iterrows():
    if row["pop1"] in all_pops and row["pop2"] in all_pops:
        mat.loc[row["pop1"], row["pop2"]] = row["f3"]
        mat.loc[row["pop2"], row["pop1"]] = row["f3"]

# Create ordered list by group
ordered_pops = []
seen = set()
for group_name, pattern in group_order:
    for p in all_pops:
        if p not in seen and pattern.search(p):
            ordered_pops.append(p)
            seen.add(p)
# (If there are any stray pops, append them at end)
for p in all_pops:
    if p not in seen:
        ordered_pops.append(p)

# Reindex the matrix
mat = mat.reindex(index=ordered_pops, columns=ordered_pops)

# Mask diagonal
data = mat.values.copy()
mask = np.eye(len(ordered_pops), dtype=bool)
data[mask] = np.nan

# --- Plot heatmap ---
plt.figure(figsize=(10, 8))
plt.imshow(data, aspect="auto", interpolation="none")
plt.colorbar(label="f₃ statistic")
plt.xticks(range(len(ordered_pops)), ordered_pops, rotation=90)
plt.yticks(range(len(ordered_pops)), ordered_pops)
#plt.title("Pairwise outgroup-f₃ (X, Y; Mbuti)")
plt.tight_layout()
plt.show()
plt.savefig("qp3pop_f3.png", dpi=300)
