# 実行するサンプル名をリストとして指定する
list=(
    #"F23.bam"
    #"I15.bam"
    #"FM020_sorted.bam"
    #"NA18939.bam"
    #"Iyai4b_Dra.bam"
    #"Todo5_Dra.bam"
    #"T5_human.bam"
    #"I4_human.bam"
    "FM027-1.bam"
    "FM027-2.bam"
)

# リストのサンプル名とを一つずつ取り出して実行
for i in "${list[@]}"
do
    # サンプル名を取り出す
    BAMFILE=$(echo $i | awk '{print $1}')
    # ここで実行する
    /home/mkato/mkato-jomon/2-msmc/2a-0-bam_to_hetsep.sh $BAMFILE 
done
