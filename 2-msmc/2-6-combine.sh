sample1="FM020_sorted"
sample2="NA18939"

popDIR=/home1/mkato/hdd_data/data/2-msmc/
DIR=/home1/mkato/hdd_data/data/2-msmc/${sample1}_${sample2}/separate_history



/home/mkato/Repo/msmc/msmc-tools/combineCrossCoal.py $DIR/${sample1}_${sample2}.msmc2.final.txt $popDIR/${sample1}/effective_population_size_file/${sample1}.msmc2.final.txt \
	$popDIR/${sample2}/effective_population_size_file/${sample2}.msmc2.final.txt > $DIR/${sample1}_${sample2}.combined.msmc2.final.txt
