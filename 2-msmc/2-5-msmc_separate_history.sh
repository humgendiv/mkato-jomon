DATADIR="/home/mkato/hdd_data/data/2-msmc/"
sample2="NA18939"
sample1="F23"
INPUTDIR="${DATADIR}/${sample1}_${sample2}/msmc_input_file/"
OUTDIR="${DATADIR}/${sample1}_${sample2}/separate_history/"
mkdir -p $OUTDIR

/usr/local/bin/msmc2 -t 20 -s -o $OUTDIR/${sample1}_${sample2}.msmc2 $INPUTDIR/${sample1}_joined_to_${sample2}.{1..22}.multihetsep.txt
