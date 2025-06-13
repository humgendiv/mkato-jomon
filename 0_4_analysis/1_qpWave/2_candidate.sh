#!/usr/bin/env bash
target="Japan_MidAndLate_Jomon"
source1="Japan_Early_Jomon"
candidates=( Japan_KumaNishioda_Yayoi Japan_Honshu_Kofun Japanese Korean Korea_Ando \
             Korea_Changhang Korea_Taejungni Korea_Yokchido Korea_Yondaedo )

outgroups="Mbuti.DG Russia_Ust_Ishim Russia_Kostenki14 Russia_MA1_HG \
Papuan Karitiana Russia_DevilsCave_N China_Tianyuan"

# Outgroup 一度だけ書き出し
echo ${outgroups} | tr ' ' '\n' > right.pops

for src2 in "${candidates[@]}"; do
  echo "▶ Testing $src2"

  # ---- qpWave② 用 Left (Target+Sources) ----
  echo $target $source1 $src2 | tr ' ' '\n' > left.TS.pops

  /home/mkato/Repo/AdmixTools/bin/qpWave -p 1p_qpWave2.par > qpwave_$src2.out
  
  rank1p=$(awk '
  $1=="f4rank:" && $2==1 {
      for(i=1;i<=NF;i++) if($i=="tail:"){print $(i+1); exit}
  }' "qpwave_${src2}.out")

  if [[ -z "${rank1p}" ]]; then
  echo "  ⚠ rank1 tail P not found — skip ${src2}"
  continue
  fi
  printf "  rank1 tail P = %s\n" "${rank1p}"


  # rank1 が受容域 (>0.05) だけ qpAdm へ
  awk 'BEGIN{if('$rank1p' > 0.05) exit 0; else exit 1}'
  if [ $? -eq 0 ]; then
    /home/mkato/Repo/AdmixTools/bin/qpAdm -p 1p_qpAdm.par > qpadm_$src2.out
    grep -E "tail prob|best coefficients" qpadm_$src2.out
  fi
done
