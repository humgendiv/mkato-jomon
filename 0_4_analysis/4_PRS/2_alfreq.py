"""
ポリジェニックスコア計算の前段階として、
入力するデータのを頻度データに変換し、後の計算を高速化できるようにする。

入力データパス
jomon = "/home/mkato/hdd_data/0_4_analysis/4_PRS/merged.prs.renamed.vcf.gz"
modern_jpt = "/home/mkato/hdd_data/data/Genomes1000/jptvcf_bed_extracted/merged/m_jpt_extracted_alfreq.vcf"
modern_jptのほうはすでにアリル頻度が計算されており、それは8列目のFORMAT列にAF=0.123のような形式で格納されている。
それぞれの入力ファイルは#から始まるコメント行が多数冒頭に含まれていることに留意されたし。
"""

# 縄文人データについて、各個体を扱うかどうかと、各個体をどのような集団としてまとめるか明示する。
# 今回は全個体を使い、Iyai（Iで始まる個体）を1集団として扱い、他の個体を全てそれ以外の集団としてまとめる。
# Iyai集団はIyaiとし、それ以外はOtherJomonとする。

# 各集団における各サイトの遺伝子頻度を計算する。なお遺伝子頻度とは、0/1,1/0のとき0.5, 1/1のとき1, 0/0のとき0と扱う。これらを集団内で平均したものが値となる。

# 生成フォーマットは、1列目から順に、ID, REF, ALT, Iyai, OtherJomonの順で、各列はタブ区切りとする。IyaiとOtherJomonはそれぞれの集団における各サイトの遺伝子頻度を表す0から1のいずれかの値を持つ。

# 出力したファイルはmodern_jptの内容と結合させ（Iyai, OtherJomonのとなりにModernJapaneseがあるように）、/home/mkato/hdd_data/0_4_analysis/4_PRS/alfreq.tsvとして保存する。

import gzip
import re

def parse_jomon_vcf(file_path):
    """縄文人VCFファイルを解析し、個体情報と遺伝子頻度を計算"""
    variants = []
    
    with gzip.open(file_path, 'rt') as f:
        sample_names = []
        
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                if line.startswith('#CHROM'):
                    # サンプル名を取得
                    sample_names = line.split('\t')[9:]
                continue
            
            fields = line.split('\t')
            chrom = fields[0]
            pos = fields[1]
            variant_id = fields[2]
            ref = fields[3]
            alt = fields[4]
            
            # 遺伝子型データを解析
            genotypes = fields[9:]
            
            # IyaiとOtherJomonに分類
            iyai_genotypes = []
            other_jomon_genotypes = []
            
            for i, genotype in enumerate(genotypes):
                sample_name = sample_names[i]
                gt = genotype.split(':')[0]  # GT field
                
                if gt in ['0/0', '0|0']:
                    allele_freq = 0.0
                elif gt in ['0/1', '1/0', '0|1', '1|0']:
                    allele_freq = 0.5
                elif gt in ['1/1', '1|1']:
                    allele_freq = 1.0
                else:
                    continue  # missing data
                
                if sample_name.startswith('I'):
                    iyai_genotypes.append(allele_freq)
                else:
                    other_jomon_genotypes.append(allele_freq)
            
            # 集団内平均頻度を計算
            iyai_freq = sum(iyai_genotypes) / len(iyai_genotypes) if iyai_genotypes else 0.0
            other_jomon_freq = sum(other_jomon_genotypes) / len(other_jomon_genotypes) if other_jomon_genotypes else 0.0
            
            # バリアント情報を保存
            variant_info = {
                'id': f"{chrom}:{pos}",
                'ref': ref,
                'alt': alt,
                'iyai': iyai_freq,
                'other_jomon': other_jomon_freq
            }
            variants.append(variant_info)
    
    return variants

def parse_modern_jpt_vcf(file_path):
    """現代日本人VCFファイルを解析し、AF値を抽出"""
    variants = {}
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue
            
            fields = line.split('\t')
            chrom = fields[0]
            pos = fields[1]
            ref = fields[3]
            alt = fields[4]
            info = fields[7]
            
            # AF値を抽出
            af_match = re.search(r'AF=([0-9.]+)', info)
            if af_match:
                af_value = float(af_match.group(1))
                variant_id = f"{chrom}:{pos}"
                variants[variant_id] = {
                    'ref': ref,
                    'alt': alt,
                    'af': af_value
                }
    
    return variants

def merge_and_output(jomon_variants, modern_variants, output_path):
    """データをマージして出力"""
    with open(output_path, 'w') as f:
        # ヘッダー
        f.write("ID\tREF\tALT\tIyai\tOtherJomon\tModernJapanese\n")
        
        for variant in jomon_variants:
            variant_id = variant['id']
            ref = variant['ref']
            alt = variant['alt']
            iyai = variant['iyai']
            other_jomon = variant['other_jomon']
            
            # 対応する現代日本人データがある場合のみ出力
            if variant_id in modern_variants:
                modern_af = modern_variants[variant_id]['af']
                f.write(f"{variant_id}\t{ref}\t{alt}\t{iyai:.4f}\t{other_jomon:.4f}\t{modern_af:.4f}\n")

def main():
    # パス設定
    jomon_file = "/home/mkato/hdd_data/0_4_analysis/4_PRS/merged.prs.renamed.vcf.gz"
    modern_jpt_file = "/home/mkato/hdd_data/data/Genomes1000/jptvcf_bed_extracted/merged/m_jpt_extracted_alfreq.vcf"
    output_file = "/home/mkato/hdd_data/0_4_analysis/4_PRS/alfreq.tsv"
    
    print("縄文人VCFファイルを解析中...")
    jomon_variants = parse_jomon_vcf(jomon_file)
    print(f"縄文人データ: {len(jomon_variants)} variants")
    
    print("現代日本人VCFファイルを解析中...")
    modern_variants = parse_modern_jpt_vcf(modern_jpt_file)
    print(f"現代日本人データ: {len(modern_variants)} variants")
    
    print("データをマージして出力中...")
    merge_and_output(jomon_variants, modern_variants, output_file)
    print(f"出力完了: {output_file}")

if __name__ == "__main__":
    main()