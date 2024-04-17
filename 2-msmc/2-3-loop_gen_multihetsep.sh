for chr in {1..22}
do
    #qsub -v chr=$chr ./2-2-gen_multihetsep.sh
    #qsub -v chr=$chr ./2-2-gen_multihetsep.sh
    qsub -v chr=$chr,sample=FM020_sorted,sample_ref=NA18939 ./2-2-gen_multihetsep.sh
    qsub -v chr=$chr,sample=F23,sample_ref=NA18939 ./2-2-gen_multihetsep.sh
    #echo "${chr}番染色体"
done
