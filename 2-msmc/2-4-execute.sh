# サンプル名のリストを指定
list=(
    #"F23"
    #"FM020_sorted"
    #"NA18939"
    #"FM027-1"
    #"FM027-2"
    "I1"
)

# リストのサンプル名を一つずつ取り出して実行
for i in "${list[@]}"
do
    # サンプル名を取り出す
    SAMPLE=$(echo $i)
    # ここで実行する
    qsub -v sample=$SAMPLE 2-4-msmc_popsize.sh
done
