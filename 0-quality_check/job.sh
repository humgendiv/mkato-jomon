SAMPLES=("FM020" "F23" "I4" "T5")

for SAMPLE in "${SAMPLES[@]}"
do
    qsub -v SAMPLE=$SAMPLE /home/mkato/mkato-jomon/0-quality_check/0-0-stats.sh
done