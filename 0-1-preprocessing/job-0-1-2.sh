SAMPLES=("FM020" "F23_1to8" "F23_9to22" "I4" "T5")

for SAMPLE in "${SAMPLES[@]}"
do
    qsub -v SAMPLE=$SAMPLE /home/mkato/mkato-jomon/0-1-preprocessing/0-1-2-master_bim_extract.sh
done