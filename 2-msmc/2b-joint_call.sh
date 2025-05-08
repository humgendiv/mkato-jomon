#!/bin/bash
# run_joint_call.sh
# 2つのBAMファイルから共通callable領域を定義しjoint callingを行い、
# さらにMSMC2解析用のmultihetsepファイルを生成するパイプライン
#
# ※ FM020_sorted.bam では染色体名に "chr" が付与されていますが、
#    F23.bam では染色体名に "chr" が付いていないため、F23の深度情報を変換します。
#
# 必要なツール:
#   - samtools
#   - bcftools
#   - bedtools
#   - generate_multihetsep.py (MSMC2付属スクリプト)
#
# 各パス、閾値は環境に合わせて調整してください。

# 1. 入力ファイル、リファレンス、出力ディレクトリの設定
BAM1="/home/mkato/hdd_data/data/bam/share/FM020_sorted.bam"
BAM2="/home/mkato/hdd_data/data/bam/share/F23.bam"
REF="/home/mkato/hdd_data/data/reference/hs37d5_chr.fa"  # リファレンスFASTAのパス
REF_mask="/home/mkato/hdd_data/data/reference/ref_masks"  # リファレンスのmaskファイルの格納フォルダパス
OUTDIR="/home/mkato/hdd_data/data/2-msmc/joint_calling"
mkdir -p "${OUTDIR}"

MSMC_TOOLS=/home/mkato/Repo/msmc/msmc-tools/

# callable領域のカバレッジ閾値（例：10×～100×）
MINCOV=10
MAXCOV=100

echo "=== Step 1: 各BAMの深度情報を取得 ==="
#samtools depth -a "${BAM1}" > "${OUTDIR}/FM020_sorted.depth.txt"
#samtools depth -a "${BAM2}" > "${OUTDIR}/F23.depth.txt"

echo "=== Step 2: F23の深度情報の染色体名を 'chr' 付きに変換 ==="
# F23.depth.txt の1列目が染色体番号のみの場合、'chr'を付与
# awk '{
#     if($1 !~ /^chr/) {
#         $1 = "chr" $1
#     }
#     print
# }' "${OUTDIR}/F23.depth.txt" > "${OUTDIR}/F23.depth.mod.txt"

echo "=== Step 3: 各サンプルのcallable領域(mask)を作成 ==="
# 各行のカバレッジがMINCOV～MAXCOVの位置をBED形式に変換（0-based start）
# awk -v min=${MINCOV} -v max=${MAXCOV} '$3>=min && $3<=max {print $1"\t"$2-1"\t"$2}' "${OUTDIR}/FM020_sorted.depth.txt" > "${OUTDIR}/FM020_sorted.mask.bed"
# awk -v min=${MINCOV} -v max=${MAXCOV} '$3>=min && $3<=max {print $1"\t"$2-1"\t"$2}' "${OUTDIR}/F23.depth.mod.txt" > "${OUTDIR}/F23.mask.bed"
echo "=== Step 3-2: 各maskファイルをソート・マージして連続区間にまとめる ==="
#sort -k1,1 -k2,2n "${OUTDIR}/FM020_sorted.mask.bed" | bedtools merge > "${OUTDIR}/FM020_sorted.mask.merged.bed"
#sort -k1,1 -k2,2n "${OUTDIR}/F23.mask.bed" | bedtools merge > "${OUTDIR}/F23.mask.merged.bed"

echo "=== Step 4: 両サンプルで共通のcallable領域を取得 ==="
#bedtools intersect -a "${OUTDIR}/FM020_sorted.mask.merged.bed" -b "${OUTDIR}/F23.mask.merged.bed" > "${OUTDIR}/common_callable.bed"
# if [ ! -s "${OUTDIR}/common_callable.bed" ]; then
#     echo "エラー: 共通のcallable領域が空です。maskの生成やマージに問題がないか確認してください。"
#     exit 1
# fi
# echo "共通callable領域行数: $(wc -l < "${OUTDIR}/common_callable.bed")"

# echo "=== Step 5: bcftoolsで共通領域に限定したjoint variant callingを実施 ==="
# # -R オプションで共通callable領域に限定してvariant calling
# bcftools mpileup -f "${REF}" -R "${OUTDIR}/common_callable.bed" "${BAM1}" "${BAM2}" | bcftools call -mv -Ov -o "${OUTDIR}/joint_calls.vcf"
# if [ $? -ne 0 ]; then
#     echo "エラー：joint variant callingが失敗しました。"
#     exit 1
# fi

# for chr in {1..22}; do
# (
# bcftools mpileup -f "${REF}" -R <(grep "^chr${chr}" "${OUTDIR}/common_callable.sorted.bed")  "${BAM1}" "${BAM2}" | \
# bcftools call -c -V indels | \
# $MSMC_TOOLS/bamCaller.py 45 "${OUTDIR}/pair_mask.chr${chr}.bed.gz" | \
# gzip -c > "${OUTDIR}/pair_calls.chr${chr}.vcf.gz"
# )&
# done
# wait
# if [ $? -ne 0 ]; then
#     echo "エラー：joint variant callingが失敗しました。"
#     exit 1
# fi

echo "=== Step 6: generate_multihetsep.pyで各サンプルのmultihetsepファイルを生成 ==="
# 共通maskとjoint VCFを用いて、各サンプルのmultihetsepファイルを生成

for chr in {2..22}; do
(
echo generate multihetsep chr${chr}
$MSMC_TOOLS/generate_multihetsep.py \
--chr ${chr} \
--mask "${OUTDIR}/pair_mask.chr${chr}.bed.gz" \
--mask $REF_mask/hs37d5_chr${chr}.mask.bed \
"${OUTDIR}/pair_calls.chr${chr}.vcf.gz" \
> "${OUTDIR}/pair.chr${chr}.multihetsep.txt"
)&
done
wait
# $MSMC_TOOLS/generate_multihetsep.py --mask "${OUTDIR}/common_callable.bed" --mask "${OUTDIR}/joint_calls.vcf" -o "${OUTDIR}/FM020_sorted"
# if [ $? -ne 0 ]; then
#     echo "エラー：FM020_sortedのmultihetsepファイル生成が失敗しました。"
#     exit 1
# fi

# $MSMC_TOOLS/generate_multihetsep.py --mask "${OUTDIR}/common_callable.bed" --mask "${OUTDIR}/joint_calls.vcf" -o "${OUTDIR}/F23"
# if [ $? -ne 0 ]; then
#     echo "エラー：F23のmultihetsepファイル生成が失敗しました。"
#     exit 1
# fi

echo "=== パイプライン完了 ==="
echo "【出力ファイル】"
# echo "  - 共通callable領域 (BED): ${OUTDIR}/common_callable.bed"
echo "  - Joint VCF: ${OUTDIR}/joint_calls.vcf"
echo "  - FM020_sorted multihetsepファイル: ${OUTDIR}/FM020_sorted.*.multihetsep.txt"
echo "  - F23 multihetsepファイル: ${OUTDIR}/F23.*.multihetsep.txt"