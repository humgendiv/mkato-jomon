#!/usr/bin/env python3
#
# filter_sites_by_fid_with_summary.py
#
# 使い方:
#   pip install pysam
#   chmod +x filter_sites_by_fid_with_summary.py
#   ./filter_sites_by_fid_with_summary.py \
#       merged_with_1240K.targetpops.v4.2.vcf.gz \
#       merged_with_1240K.targetpops.filtered.summary.vcf.gz
#   tabix -p vcf merged_with_1240K.targetpops.filtered.summary.vcf.gz
#

import sys
import pysam

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} <input.vcf.gz> <output.vcf.gz>")
    sys.exit(1)

in_vcf_path  = sys.argv[1]
out_vcf_path = sys.argv[2]

vcf_in  = pysam.VariantFile(in_vcf_path,  mode='r')
vcf_out = pysam.VariantFile(out_vcf_path, mode='wz', header=vcf_in.header)

# サンプルを FID ごとにグループ化
samples = list(vcf_in.header.samples)
groups = {}
for s in samples:
    fid = s.split('_', 1)[0]
    groups.setdefault(fid, []).append(s)

# 除外カウント初期化
drop_counts = {fid: 0 for fid in groups}

total_sites = 0
kept_sites  = 0

for rec in vcf_in:
    total_sites += 1
    # 除外理由となったグループ一覧
    bad_fids = []

    for fid, samp_list in groups.items():
        # グループ内に non-missing があるかチェック
        has_called = False
        for s in samp_list:
            gt = rec.samples[s]['GT']
            if gt is None or gt == (None, None):
                continue
            has_called = True
            break
        if not has_called:
            bad_fids.append(fid)

    if bad_fids:
        # 除外：原因となった各FIDグループのカウントを増やす
        for fid in bad_fids:
            drop_counts[fid] += 1
        continue  # このサイトは出力しない

    # 出力
    vcf_out.write(rec)
    kept_sites += 1

vcf_in.close()
vcf_out.close()

# サマリ―表示
print("\n=== フィルタリング結果サマリ ===")
print(f"総サイト数: {total_sites}")
print(f"保持サイト数: {kept_sites}")
print(f"除外サイト数: {total_sites - kept_sites}\n")
print("各FIDグループごとの除外サイト数：")
for fid, cnt in sorted(drop_counts.items()):
    print(f"  {fid}: {cnt}")
print("================================\n")
