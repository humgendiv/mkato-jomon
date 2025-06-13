#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
vcf_genotype_summary.py

VCF(.vcf.gz) の各サンプルについて、ジェノタイプ（0/0, 0/1, 1/0, 1/1, ./.,
それ以外）をカウントして出力するスクリプト。

Usage:
    python util_sum_GT.py input.vcf.gz > genotype_counts.tsv
"""

import sys
import pysam

def main(vcf_path):
    # VCFを開く
    vcf = pysam.VariantFile(vcf_path)

    # サンプル名を取得
    samples = list(vcf.header.samples)

    # カウント用の初期化
    gt_types = ['0/0', '0/1', '1/0', '1/1', './.', 'OTHER']
    counts = {s: {gt: 0 for gt in gt_types} for s in samples}

    # レコードを走査
    for rec in vcf.fetch():
        for s in samples:
            gt = rec.samples[s]['GT']  # タプルで返る (allele1, allele2)
            if gt is None:
                key = './.'
            else:
                # missing は -1 または None で表現される
                alleles = []
                for a in gt:
                    if a is None or a < 0:
                        alleles.append('.')
                    else:
                        alleles.append(str(a))
                geno = '/'.join(alleles)
                key = geno if geno in counts[s] else 'OTHER'
            counts[s][key] += 1

    # ヘッダー出力
    header = ['Sample'] + gt_types
    print('\t'.join(header))

    # 各サンプルのカウント出力
    for s in samples:
        row = [s] + [str(counts[s][gt]) for gt in gt_types]
        print('\t'.join(row))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python vcf_genotype_summary.py input.vcf.gz\n")
        sys.exit(1)
    main(sys.argv[1])
