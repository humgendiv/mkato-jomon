#SAMPLES=("FM020" "F23" "I4" "T5")
SAMPLES=("FM020")
for SAMPLE in "${SAMPLES[@]}"
do
    qsub -v SAMPLE=$SAMPLE /home/mkato/mkato-jomon/0-1-preprocessing/0-1-1-0-toplink.sh
done
