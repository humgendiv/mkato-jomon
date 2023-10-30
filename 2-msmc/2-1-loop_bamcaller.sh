for chr in {1..22}
do
    qsub execute_bamcaller.sh T5 30 $chr
    echo "T5の${chr}"
    sleep 1
    qsub execute_bamcaller.sh I4 25 $chr
    echo "I4の${chr}"
    sleep 1
done