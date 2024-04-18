SAMPLES=("FM020.chr1-7" "FM020.chr8-22" "F23.chr1-7" "F23.chr8-22" "Iyai4b.chr1-7" "Iyai4b.chr8-22" "Todo5.chr1-7" "Todo5.chr8-22")

for SAMPLE in "${SAMPLES[@]}"
do
    qsub -v SAMPLE=$SAMPLE /home/mkato/mkato-jomon/0-1-preprocessing/0-1-2-master_bim_extract.sh
done
