DIR=/home1/mkato/hdd_data/data/
INPUT_DIR=${DIR}/0-2-plink
OUTPUT_DIR=${DIR}/PS/jomon_prs/

mkdir -p ${OUTPUT_DIR}

# 多少フィルターをかけたとはいえまだまだデータサイズが大きいので、prsでつかうSNPで
# のBIMファイルの全結合データを使ってBIM約１００MB分までデータサイズを削減する。
/usr/local/bin/plink --make-bed --extract ${DIR}/PS/unique_snps.txt \
--bfile ${INPUT_DIR}/${SAMPLE} --out ${OUTPUT_DIR}/${SAMPLE}
