# 前処理を一括で実行するスクリプト

# 用いる個体のリストを指定
sample_list=["F23", "FM020", "Iyai4b", "Todo5"]
# 各個体について、細かい処理を実行
for sample in ${sample_list[@]}; do
    # ファイルの前処理を実行
    bash 0a-1.sh ${sample}
done

