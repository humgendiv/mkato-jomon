popDIR=/home1/mkato/hdd_data/data/2-msmc/effective_population_size_file
DIR=/home1/mkato/hdd_data/data/2-msmc/separate_history

sample2="T5"
sample1="NA18939"

/home/mkato/Repo/msmc/msmc-tools/combineCrossCoal.py $DIR/${sample1}_${sample2}.msmc2.final.txt $popDIR/${sample1}.msmc2.final.txt \
    $popDIR/${sample2}.msmc2.final.txt > $DIR/${sample1}_${sample2}.combined.msmc2.final.txt