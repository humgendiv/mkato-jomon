REF=/home/mkato/hdd_data/data/Genomes1000/reference_panel/1000GP.chr${CHR}.bcf
MAP=/home/mkato/Repo/chr${CHR}.b37.gmap.gz
while IFS="" read -r LINE || [ -n "$LINE" ];
do
  printf -v ID "%02d" $(echo $LINE | cut -d" " -f1)
  IRG=$(echo $LINE | cut -d" " -f3)
  ORG=$(echo $LINE | cut -d" " -f4)

  /usr/local/bin/GLIMPSE2_split_reference_static -R ${REF} -M ${MAP} --input-region ${IRG} --output-region ${ORG} -O /home/mkato/hdd_data/data/Genomes1000/reference_panel/split/1000GP.chr${CHR}
done < /home/mkato/hdd_data/data/Genomes1000/chunks/chunks.chr${CHR}.txt