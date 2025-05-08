sample1="FM020_sorted"
sample2="F23"

popDIR=/home1/mkato/hdd_data/data/2-msmc/
DIR=/home1/mkato/hdd_data/data/2-msmc/${sample1}-${sample2}/effective_population_size_file



/home/mkato/Repo/msmc/msmc-tools/combineCrossCoal.py $DIR/${sample1}-${sample2}.msmc2.final.txt $DIR/${sample1}.msmc2.final.txt \
	$DIR/${sample2}.msmc2.final.txt > $DIR/${sample1}-${sample2}.combined.msmc2.final.txt
