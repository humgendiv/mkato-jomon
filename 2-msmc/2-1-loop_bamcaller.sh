for chr in {1..22}
do
    qsub /home/mkato/mkato-jomon/2-msmc/2-0-bamcaller.sh T5 30 $chr
    echo "T5の${chr}"
    sleep 1
    qsub /home/mkato/mkato-jomon/2-msmc/2-0-bamcaller.sh I4 25 $chr
    echo "I4の${chr}"
    sleep 1
done