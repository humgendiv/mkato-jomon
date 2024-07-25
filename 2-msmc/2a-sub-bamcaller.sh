# 染色体ごとにbamに対してmsmcを実行するための処理を実行する
# 2a-0-bamcaller.shで回すfor文の中で実行される
# このスクリプトは、2a-0-bamcaller.shから引数を受け取る
BAMFILE=$BAMFILE
DEPTH=$DEPTH
CHROM=$CHROM
# CHROMには文字列chrが入っている場合があり、数字のみで使いたい場合のためにchrを取り除く（もともと含まれていない場合はそのまま）
CHROM_WITHOUT_CHR=$(echo $CHROM | sed -e "s/chr//g")
DATADIR=/home/mkato/hdd_data/data/
# もしCHROMにchrが含まれている場合は、REFERENCEのファイル名もchrを含める
if [[ $CHROM != chr* ]]; then
    REFERENCE=$DATADIR/reference/hg19_no_chr.fa
else
    REFERENCE=$DATADIR/reference/hg19.fa
fi
MSMC_TOOLS=/home/mkato/Repo/msmc/msmc-tools/
# サンプルネームについて、BAMFILEのファイル名から拡張子を取り除いたものを取得する
SAMPLENAME=$(basename $BAMFILE .bam)
OUTDIR=$DATADIR/2-msmc/$SAMPLENAME
mkdir -p $OUTDIR

echo "Start calling SNPs and indels for $SAMPLENAME on $CHROM"
bcftools mpileup -q 20 -Q 20 -C 50 -Ou -r $CHROM -f $REFERENCE $BAMFILE | bcftools call -c -V indels | $MSMC_TOOLS/bamCaller.py $DEPTH $OUTDIR/${SAMPLENAME}_${CHROM_WITHOUT_CHR}_mask.bed.gz | gzip -c > $OUTDIR/${SAMPLENAME}_${CHROM_WITHOUT_CHR}.vcf.gz
echo "Finished calling SNPs and indels for $SAMPLENAME on $CHROM"

REF_MASK=$DATADIR/reference/ref_masks/hs37d5_chr${CHROM_WITHOUT_CHR}.mask.bed
MULTIHETSEP_OUTPUT=$OUTDIR/msmc_input_file
mkdir -p $MULTIHETSEP_OUTPUT
echo "Start generating multihetsep file for $SAMPLENAME on $CHROM"
# 以下はgen_multihetsetに順ずる。ただし、1個体のみに対して実行。複数個体を同一集団とみなして一括で実行する場合は未実装。
$MSMC_TOOLS/generate_multihetsep.py --chr $CHROM --mask=$OUTDIR/${SAMPLENAME}_${CHROM_WITHOUT_CHR}_mask.bed.gz --mask=$REF_MASK $OUTDIR/${SAMPLENAME}_${CHROM_WITHOUT_CHR}.vcf.gz > $MULTIHETSEP_OUTPUT/${SAMPLENAME}.${CHROM_WITHOUT_CHR}.multihetsep.txt

echo "Finished generating multihetsep file for $SAMPLENAME on $CHROM"
