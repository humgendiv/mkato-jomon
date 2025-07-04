#!/usr/bin/env python3
"""
calc_outgroup_f3.py  :  縄文 (A) × 47都道府県 (B) の outgroup f3(A,B;Mbuti) を計算
入力:
    1. pop_freq.tsv               (Jomon & Mbuti を含む AlleleFreq; タブ区切り)
    2. prefecture_dir/*.afreq     (#CHROM,ID,REF,ALT,ALT_FREQS,OBS_CT)

出力: TSV (Jomon,Prefecture,f3,nSNP) を標準出力

必要 python パッケージ:  pandas, numpy
"""

import os
import sys
import glob
import numpy as np
import pandas as pd

# ---------- ユーザ設定 ----------
POP_FREQ_FILE   = "/home/mkato/hdd_data/0_4_analysis/3_prefecture/pop_freq.tsv"
PREF_DIR        = "/home/mkato/hdd_data/0_4_analysis/3_prefecture/prefectural_afreq_data"
OUT_FILE      = "outgroup_f3_3x47.tsv"
JOMON_POPS      = ["Chidorigakubo","Funadomari","Iyai","Mitsusawa","Todoroki",]
OUTGROUP        = "Mbuti"
# --------------------------------

# ---------- 便利関数 ----------
def load_pop_freq(path):
    df = pd.read_csv(path, sep="\t", dtype={"CHR": str})
    df["key"] = df["CHR"].astype(str) + ":" + df["POS"].astype(str)
    meta = df[["key","CHR","REF","ALT"]].drop_duplicates("key").set_index("key")
    wide = df.pivot(index="key", columns="POP", values="AF")
    return wide, meta

def load_pref_afreq(fname, meta):
    cols = ["#CHROM","ID","REF","ALT","ALT_FREQS"]
    pref = pd.read_csv(fname, sep="\t", usecols=cols, dtype={"#CHROM": str})
    pref["key"] = pref["ID"]
    pref = pref.join(meta, on="key", how="inner", rsuffix="_ref")

    same    = (pref["REF"]==pref["REF_ref"]) & (pref["ALT"]==pref["ALT_ref"])
    flipped = (pref["REF"]==pref["ALT_ref"]) & (pref["ALT"]==pref["REF_ref"])

    pref.loc[same   , "AF_aligned"] = pref.loc[same   , "ALT_FREQS"]
    pref.loc[flipped, "AF_aligned"] = 1.0 - pref.loc[flipped, "ALT_FREQS"]

    return pref.dropna(subset=["AF_aligned"]).set_index("key")[["AF_aligned"]]

def f3(pA, pB, pO):             # 単純平均
    return np.mean((pA - pO) * (pB - pO))

def jackknife_chr(df, chr_vec, jomon, pref, outgrp):
    theta_full = f3(df[jomon].values, df[pref].values, df[outgrp].values)
    ests = []
    for c in chr_vec.unique():
        part = df.loc[chr_vec != c]
        if len(part)==0:              # その染色体しか残っていない場合
            continue
        ests.append(f3(part[jomon].values, part[pref].values, part[outgrp].values))
    n = len(ests)
    se = np.sqrt(((n-1)/n) * np.sum((ests - theta_full)**2))
    z  = theta_full / se if se>0 else np.nan
    return theta_full, se, z
# --------------------------------

def main():
    wide, meta = load_pop_freq(POP_FREQ_FILE)
    pO = wide[OUTGROUP]

    records = []

    for af in sorted(glob.glob(os.path.join(PREF_DIR, "*.afreq"))):
        pref = os.path.basename(af).split(".")[2]       # kenXX
        pB_series = load_pref_afreq(af, meta)["AF_aligned"]

        merged = wide[JOMON_POPS].join(pB_series, how="inner") \
                                  .join(pO, how="inner") \
                                  .join(meta["CHR"], how="inner")

        merged = merged.rename(columns={"AF_aligned": pref})
        chr_vec = merged["CHR"]; merged = merged.drop(columns="CHR")

        for jomon in JOMON_POPS:
            sub = merged[[jomon, pref, OUTGROUP]].dropna()
            if len(sub) == 0: continue
            f3val, se, z = jackknife_chr(sub, chr_vec.loc[sub.index],
                                         jomon, pref, OUTGROUP)
            records.append((jomon, pref, f3val, se, z, len(sub)))

    out = pd.DataFrame(records,
                       columns=["Jomon","Prefecture","f3","SE","Z","nSNP"])
    out.to_csv(OUT_FILE, sep="\t", index=False)
    print(f"✓  {OUT_FILE} に {len(out)} 行を書き出しました。")

if __name__ == "__main__":
    main()
