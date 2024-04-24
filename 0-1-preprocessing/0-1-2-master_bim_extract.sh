#!/bin/bash
#PBS -N masteer_bim_extract
#PBS -e error_file.log
#PBS -l nodes=1:ppn=1
#PBS -l walltime=10:00:00

DIR=/home1/mkato/hdd_data/data/
INPUT_DIR=${DIR}/0-0-raw_vcf/complete/plink
OUTPUT_DIR=${DIR}/0-3-extract_plink


# 多少フィルターをかけたとはいえまだまだデータサイズが大きいので、今回主に扱う１２４０Kと４７都道府県
# のBIMファイルの全結合データを使ってBIM約１００MB分までデータサイズを削減する。
/usr/local/bin/plink --make-bed --extract ${DIR}/bim/merged_positions.bim \
--bfile ${INPUT_DIR}/${SAMPLE} --out ${OUTPUT_DIR}/${SAMPLE}
