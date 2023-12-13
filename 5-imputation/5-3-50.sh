REF=/home/mkato/hdd_data/data/Genomes1000/reference_panel/split/1000GP.chr${CHR}
sample=T5
BAM=/home/mkato/hdd_data/data/bam/share/new${sample}.bam
MAP=/home/mkato/Repo/chr${CHR}.b37.gmap.gz

while IFS="" read -r LINE || [ -n "$LINE" ]; 
do   
	printf -v ID "%02d" $(echo $LINE | cut -d" " -f1)
	IRG=$(echo $LINE | cut -d" " -f3)
	ORG=$(echo $LINE | cut -d" " -f4)
	CHR=$(echo ${LINE} | cut -d" " -f2)
	REGS=$(echo ${IRG} | cut -d":" -f 2 | cut -d"-" -f1)
	REGE=$(echo ${IRG} | cut -d":" -f 2 | cut -d"-" -f2)
	OUT=/home/mkato/hdd_data/data/5-imputed/${sample}_imputed
	/usr/local/bin/GLIMPSE2_phase_static --bam-file ${BAM} --reference ${REF}_${CHR}_${REGS}_${REGE}.bin --output ${OUT}_${CHR}_${REGS}_${REGE}.bcf
done < /home/mkato/hdd_data/data/Genomes1000/chunks/chunks.chr${CHR}.txt