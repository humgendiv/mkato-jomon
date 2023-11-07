for chr in {1..22}
do
    qsub -v sample_name=T5,depth=35,chr=$chr /home/mkato/mkato-jomon/2-msmc/2-0-bamcaller.sh
    echo "T5の${chr}"
    qsub -v sample_name=I4,depth=28,chr=$chr /home/mkato/mkato-jomon/2-msmc/2-0-bamcaller.sh
    echo "I4の${chr}"
done