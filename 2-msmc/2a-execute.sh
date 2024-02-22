# 実行するサンプル名とそれに紐つくデプス（整数値）のペアをリストとして指定する
list = (
    "F23.bam 40"
    "I15.bam 40"
    "FM020_sorted.bam 30"
    "NA18939.bam 40"
    "Iyai4b_Dra.bam 30"
)

# リストのサンプル名とデプスを一つずつ取り出して実行
for i in "${list[@]}"
do
    # サンプル名とデプスを取り出す
    BAMFILE=$(echo $i | awk '{print $1}')
    DEPTH=$(echo $i | awk '{print $2}')
    # デプスを取り出す
    # ここで実行する
    ./2a-0-bam_to_hetsep.sh $BAMFILE $DEPTH
done
