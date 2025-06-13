#!/usr/bin/env python3
"""
vcf2popfreq.py  :  集団別アリルカウント／頻度を TSV 出力
必要: cyvcf2 (pip install cyvcf2), pandas
使い方:
    python 0_0_vcf2popfreq.py /home/mkato/hdd_data/0_4_analysis/3_prefecture/merged_with_1240K.targetpops.vcf > /home/mkato/hdd_data/0_4_analysis/3_prefecture/pop_freq.tsv
"""
import sys
from collections import defaultdict, Counter
from cyvcf2 import VCF

def get_pop(sample_name):
    """sampleID_pop → pop 部分を返す（最後の '_' 以降）"""
    return sample_name.rsplit('_', 1)[0]

def main(vcf_path):
    vcf = VCF(vcf_path)
    samples = vcf.samples
    pop_of = {s: get_pop(s) for s in samples}

    # pop -> index list
    idx_by_pop = defaultdict(list)
    for i, s in enumerate(samples):
        idx_by_pop[pop_of[s]].append(i)

    # 出力ヘッダ
    print("\t".join(["CHR","POS","REF","ALT","POP","AC","AN","AF"]))

    for variant in vcf:
        # bi-allelic のみ
        if len(variant.ALT) != 1:
            continue
        ref, alt = variant.REF, variant.ALT[0]
        genos = variant.genotypes  # list of (allele1, allele2, phased?)
        for pop, idxs in idx_by_pop.items():
            ac = an = 0
            for i in idxs:
                g = genos[i][:2]
                if -1 in g:        # missing
                    continue
                ac += g.count(1)   # ALT = 1
                an += 2
            if an == 0:
                continue
            af = ac / an
            print("\t".join(map(str, [variant.CHROM, variant.POS, ref, alt,
                                      pop, ac, an, f"{af:.6g}"])))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: vcf2popfreq.py input.vcf.gz")
    main(sys.argv[1])
