# サンプル名のリストを指定
list=(
joined
)

# リストのサンプル名を一つずつ取り出して実行
for i in "${list[@]}"
do
    # サンプル名を取り出す
    SAMPLE=$(echo $i)
    # ここで実行する
    qsub -v sample=$SAMPLE 2-4a-joined_msmc_pop.sh
done
