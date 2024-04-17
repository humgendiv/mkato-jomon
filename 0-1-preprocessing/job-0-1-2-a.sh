SAMPLES=("F23_1to8" "F23_9to22" "I4" "T5" "FM020_1to8" "FM020_9to22")

for SAMPLE in "${SAMPLES[@]}"
do
    qsub -v SAMPLE=$SAMPLE /home/mkato/mkato-jomon/0-1-preprocessing/0-1-2-a-prs_bim_extract.sh
done
