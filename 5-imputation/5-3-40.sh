REF=/home/mkato/hdd_data/data/Genomes1000/reference_panel/1000GP.chr${CHR}.bcf
MAP=../maps/genetic_maps.b38/chr22.b38.gmap.gz
while IFS="" read -r LINE || [ -n "$LINE" ];
do
  printf -v ID "%02d" $(echo $LINE | cut -d" " -f1)
  IRG=$(echo $LINE | cut -d" " -f3)
  ORG=$(echo $LINE | cut -d" " -f4)

  /usr/local/bin/GLIMPSE2_split_reference_static -R ${REF} -M ${MAP} --input-region ${IRG} --output-region ${ORG} -O reference_panel/split/1000GP.chr${CHR}
done < chunks.chr${CHR}.txt