for chr in {1..22}
do
    qsub -v chr=$chr,sample=T5 ./2-2-gen_multihetsep.sh
    #qsub -v chr=$chr,sample=I4 ./2-2-gen_multihetsep.sh
    echo "${chr}番染色体"
done
