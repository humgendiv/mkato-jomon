for chr in {1..22}
do
    qsub -v chr=$chr ./2-2-gen_multihetsepscript.sh
    echo "${chr}番染色体"
done