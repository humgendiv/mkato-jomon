#!/bin/bash

# サンプルが存在するベースディレクトリ
BASE_DIR="/home/mkato/hdd_data/0-genome_data"
# 出力先ディレクトリ
OUTPUT_DIR="/home/mkato/hdd_data/2-5-HBD/ROH"
# 使用するPLINKバイナリのパス（適宜変更）
PLINK_PATH="/usr/local/bin/plink"

# サンプルディレクトリを順に探索
for SAMPLE_DIR in ${BASE_DIR}/*/; do
    # サンプルディレクトリ名からサンプル名を抽出（最後のスラッシュを取り除く）
    SAMPLE=$(basename "${SAMPLE_DIR}")
    PROCESSED_DIR="${SAMPLE_DIR}/processed"

    # 各サンプルのprocessedフォルダ内の.bedファイルを順に処理
    for FILE in ${PROCESSED_DIR}/*.bed; do
        # 拡張子を取り除いたファイル名を取得
        FILE_BASENAME=$(basename "${FILE}" .bed)
        
        # 出力ファイルのパスを生成
        OUTPUT_FILE="${OUTPUT_DIR}/${FILE_BASENAME}_ROH"

        # PLINKのROH解析をバックグラウンドで実行
        ${PLINK_PATH} --bfile "${PROCESSED_DIR}/${FILE_BASENAME}" --homozyg --homozyg-kb 500 --homozyg-snp 50 --out "${OUTPUT_FILE}" &
        echo "Started ROH calculation for ${SAMPLE} (${FILE_BASENAME})"
    done
done

# 全ての並列処理が完了するまで待機
wait

echo "All ROH calculations completed."
