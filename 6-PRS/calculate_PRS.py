import os
import gzip
import pandas as pd

# 入力ファイルのディレクトリパス
trait_dir = "/home/mkato/hdd_data/data/PS/PRS_processed"
vcf_file = "/home/mkato/hdd_data/data/0-4-merge_and_convert/m_0-3-extract_plink.vcf"
freq_file = "/home/mkato/hdd_data/data/Genomes1000/jptvcf_bed_extracted/merged/m_jpt_extracted_alfreq.vcf"
# 出力ファイルのディレクトリパス
output_dir = "/home/mkato/hdd_data/data/PS/PRS_scores"

# P値の閾値リスト
p_thresholds = [0.01, 0.001, 0.0001]

# 縄文人個体のvcfファイルからSNPと個体名を取得
vcf_snps = {}
sample_names = []
with open(vcf_file, "r") as f:
    for line in f:
        if line.startswith("#CHROM"):
            sample_names = line.strip().split("\t")[9:]
        elif not line.startswith("#"):
            fields = line.strip().split("\t")
            snp = f"{fields[0]}:{fields[1]}"
            genotypes = fields[9:]
            if "./." not in genotypes:  # 欠損している個体が存在する行を除外
                vcf_snps[snp] = genotypes

# 日本人集団のアリル頻度を取得
freq_snps = {}
with open(freq_file, "r") as f:
    for line in f:
        if not line.startswith("#"):
            fields = line.strip().split("\t")
            snp = f"{fields[0]}:{fields[1]}"
            af = float(fields[7].split("=")[1])
            freq_snps[snp] = af

# 各P値の閾値について処理を行う
for p_threshold in p_thresholds:
    # 結果を格納するデータフレームを初期化
    result_df = pd.DataFrame(index=sample_names + ["Japanese"])
    
    # 各形質のファイルを処理
    for filename in os.listdir(trait_dir):
        if filename.endswith(".txt"):
            trait_name = filename[:-4]
            trait_file = os.path.join(trait_dir, filename)
            
            # 形質ファイルからSNPとBETAの値を取得
            trait_snps = {}
            with open(trait_file, "r") as f:
                next(f)  # ヘッダー行をスキップ
                for line in f:
                    fields = line.strip().split("\t")
                    snp = fields[0]
                    beta = float(fields[5])
                    p = float(fields[6])
                    if p <= p_threshold:
                        trait_snps[snp] = beta
            
            # 共通のSNPを取得
            common_snps_vcf = set(vcf_snps.keys()) & set(trait_snps.keys())
            common_snps_freq = set(freq_snps.keys()) & set(trait_snps.keys())
            
            # ポリジェニックスコアを計算
            prs_scores_jomon = [0] * len(sample_names)
            for snp in common_snps_vcf:
                beta = trait_snps[snp]
                genotypes = vcf_snps[snp]
                for i, genotype in enumerate(genotypes):
                    alleles = genotype.split("/")
                    if "." not in alleles:
                        dosage = alleles.count("1")
                        prs_scores_jomon[i] += beta * dosage / 2

            # 日本人個体のポリジェニックスコアを計算
            prs_score_japanese = 0
            for snp in common_snps_freq:
                beta = trait_snps[snp]
                af = freq_snps[snp]
                prs_score_japanese += beta * af

            result_df[trait_name] = prs_scores_jomon + [prs_score_japanese]
    
    # 計算対象となったSNPの数を取得
    num_snps_vcf = len(common_snps_vcf)
    num_snps_freq = len(common_snps_freq)
    
    # 結果をファイルに出力
    output_file = os.path.join(output_dir, f"PRS_scores_p{p_threshold}.txt")
    with open(output_file, "w") as f:
        f.write(f"# Number of SNPs used for Jomon: {num_snps_vcf}\n")
        f.write(f"# Number of SNPs used for Japanese: {num_snps_freq}\n")
        result_df.to_csv(f, sep="\t", index_label="Individual")
