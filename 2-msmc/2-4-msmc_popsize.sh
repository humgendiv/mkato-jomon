#!/bin/bash

#$ -cwd
#$ -V
#$ -l short
#$ -l d_rt=01:00:00
#$ -l s_rt=01:00:00
#$ -l s_vmem=32G
#$ -l mem_req=32G
#$ -N msmc
#$ -S /bin/bash


DATADIR=/home/mkato/hdd_data/data/2-msmc/

INPUTDIR=$DATADIR/msmc_input_file/
OUTDIR="${DATADIR}effective_population_size_file/"

if [ ! -d $OUTDIR ]; then
    mkdir -p $OUTDIR
fi

sample=T5I4

msmc2 -t 8 -p 1*2+15*1+1*2 -o $OUTDIR/$sample.msmc2 $INPUTDIR/$sample.chr{1..22}.multihetsep.txt