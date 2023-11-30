for chr in {1..22}; do
    qsub -v chr=$chr 5-1-collect_1000JPT.sh
done