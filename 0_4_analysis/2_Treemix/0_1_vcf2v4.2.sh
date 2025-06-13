#!/usr/bin/env bash
set -e

INVCF=/home/mkato/hdd_data/0_4_analysis/2_Treemix/merged_with_1240K.targetpops.vcf.gz
OUTVCF=/home/mkato/hdd_data/0_4_analysis/2_Treemix/merged_with_1240K.targetpops.v4.2.vcf.gz

# 1) 全行を展開して、ヘッダー行（## で始まる行）にだけ置換をかけ、再圧縮
zcat "${INVCF}" \
  | sed '/^##/s/v4\.3/v4\.2/g' \
  | bgzip -c > "${OUTVCF}"

# 2) タブ圧縮ファイルなので、必ずインデックスを再作成
tabix -p vcf -f "${OUTVCF}"

echo "written ${OUTVCF} and indexed"

