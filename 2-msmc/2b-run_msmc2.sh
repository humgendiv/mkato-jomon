#!/bin/bash
# run_msmc2.sh
# このスクリプトは、joint callingパイプラインで生成された multihetsep ファイルを用いて
# MSMC2 を実行し、全ハプロタイプ解析および個体ごとグループ化解析を行います。
#
# 前提:
#  - FM020_sorted のmultihetsepファイルは /home/mkato/hdd_data/data/2-msmc/joint_calling/FM020_sorted.*.multihetsep.txt
#  - F23 のmultihetsepファイルは /home/mkato/hdd_data/data/2-msmc/joint_calling/F23.*.multihetsep.txt
#  - MSMC2 の実行ファイルは /usr/local/bin/msmc2 として利用可能
#  - 結果は /home/mkato/hdd_data/data/2-msmc/FM020_sorted-F23-msmc2 に出力

# パス設定
INPUT_DIR="/home/mkato/hdd_data/data/2-msmc/joint_calling"
OUTPUT_DIR="/home/mkato/hdd_data/data/2-msmc/FM020_sorted-F23-msmc2"
MSMC2="/usr/local/bin/msmc2"

mkdir -p "${OUTPUT_DIR}"

# 使用するmultihetsepファイルのパス設定
FM020_FILES="${INPUT_DIR}/FM020_sorted.*.multihetsep.txt"
F23_FILES="${INPUT_DIR}/F23.*.multihetsep.txt"

echo "【MSMC2解析開始】"
echo "FM020_sortedのmultihetsepファイル: ${FM020_FILES}"
echo "F23のmultihetsepファイル: ${F23_FILES}"

#############################
# (1) 全ハプロタイプ解析 (msmc2_all)
#############################
echo "→ 全ハプロタイプ解析 (msmc2_all) を実行中..."
${MSMC2} -i 20 -t 8 -I 0,1,2,3 -o "${OUTPUT_DIR}/msmc2_all" ${FM020_FILES} ${F23_FILES}
if [ $? -ne 0 ]; then
    echo "エラー：msmc2_all の実行に失敗しました。"
    exit 1
fi
echo "→ msmc2_all の解析が完了しました。結果は ${OUTPUT_DIR}/msmc2_all.* に出力されています。"

#############################
# (2) 個体ごとグループ化解析 (msmc2_split)
#############################
echo "→ 個体ごとグループ化解析 (msmc2_split) を実行中..."
# -I 0-1,2-3 と指定することで、最初のサンプル（FM020_sorted）のハプロタイプをグループ化し、
# 次のサンプル（F23）のハプロタイプをグループ化します。
${MSMC2} -i 20 -t 8 -I 0-1,2-3 -o "${OUTPUT_DIR}/msmc2_split" ${FM020_FILES} ${F23_FILES}
if [ $? -ne 0 ]; then
    echo "エラー：msmc2_split の実行に失敗しました。"
    exit 1
fi
echo "→ msmc2_split の解析が完了しました。結果は ${OUTPUT_DIR}/msmc2_split.* に出力されています。"

echo "【MSMC2解析完了】"
echo "全ての結果は ${OUTPUT_DIR} に保存されています。"
