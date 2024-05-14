SAMPLES=("FM020.chr1-7_extracted" "FM020.chr8-22_extracted" "F23.chr1-7_extracted" "F23.chr8-22_extracted" "Iyai4b.chr1-7_extracted" "Iyai4b.chr8-22_extracted" "Todo5.chr1-7_extracted" "Todo5.chr8-22_extracted")
for SAMPLE in "${SAMPLES[@]}"
do
    qsub -v SAMPLE=$SAMPLE /home/mkato/mkato-jomon/0-1-preprocessing/0-1-2-bim_extract.sh
done
