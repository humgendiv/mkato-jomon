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

INPUTDIR=$DATADIR/FM020_sorted-F23/
OUTDIR=$INPUTDIR/effective_population_size_file/

if [ ! -d $OUTDIR ]; then
    mkdir -p $OUTDIR
fi

sample="FM020_sorted-F23"
#/usr/local/bin/msmc2 -t 20 -p 1*2+20*2+10*1 -o $OUTDIR/$sample.msmc2 $INPUTDIR/$sample.{1..22}.multihetsep.txt
#/usr/local/bin/msmc2 -t 20 -p 1*2+15*1+1*2 -o $OUTDIR/$sample.msmc2 $INPUTDIR/$sample.chr{1..20}.multihetsep.txt
#/usr/local/bin/msmc2 -t 20 -p 1*2+15*1+1*2 -o $OUTDIR/FM020.msmc2 -I 0,1 $INPUTDIR/$sample.chr{1..20}.multihetsep.txt
/usr/local/bin/msmc2 -t 20 -p 1*4+35*2+1*4 -o $OUTDIR/FM020_sorted.msmc2 -I 0,1 $INPUTDIR/$sample.chr{1..20}.multihetsep.txt
/usr/local/bin/msmc2 -t 20 -p 1*4+35*2+1*4 -o $OUTDIR/F23.msmc2 -I 2,3 $INPUTDIR/$sample.chr{1..20}.multihetsep.txt
/home/mkato/mkato-jomon/2-msmc/msmc2_Linux -t 20 -s -p 1*4+35*2+1*4 -o $OUTDIR/FM020_sorted-F23.msmc2 -I 0-2,0-3,1-2,2-3 $INPUTDIR/$sample.chr{1..20}.multihetsep.txt
