
sample=I4
LST=/home/mkato/hdd_data/data/5-imputed/GLIMPSE_ligate/list.chr${CHR}.txt
ls -1v /home/mkato/hdd_data/data/5-imputed/${sample}_imputed/${sample}_imputed_*.bcf > ${LST}

OUT=/home/mkato/hdd_data/data/5-imputed/GLIMPSE_ligate/${sample}_chr${CHR}_ligated.bcf
/usr/local/bin/GLIMPSE2_ligate --input ${LST} --output $OUT

