DATADIR="/home/mkato/hdd_data/data/2-msmc/"

INPUTDIR="${DATADIR}/msmc_input_file/"
OUTDIR="${DATADIR}/separate_history/"

sample1="NA18939"
sample2="I4"

/usr/local/bin/msmc2 -t 8 -s -o $OUTDIR/${sample1}_${sample2}.msmc2 $INPUTDIR/${sample1}_${sample2}.chr{1..22}.multihetsep.txt