#!/usr/bin/env bash

DATADIR="/home/mkato/hdd_data/data/2-msmc/"

INPUTDIR="${DATADIR}/msmc_input_file/"
OUTDIR="${DATADIR}/separate_history/"

/usr/local/bin/msmc2 -t 8 -I 0-4,0-5,1-4,1-5 -s -p 1*2+15*1+1*2 -o $OUTDIR/T5I4.msmc2 $INPUTDIR/T5I4.chr{1..22}.multihetsep.txt