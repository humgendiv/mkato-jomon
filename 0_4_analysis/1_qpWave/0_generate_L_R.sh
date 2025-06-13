#!/usr/bin/env bash
###############################################################################
# 変数をまとめて定義
###############################################################################
# 推定対象（必ず 1 集団）
target="Japan_MidAndLate_Jomon"

# 参照ソース（≥2 集団、半角スペース区切り）
sources="Japan_Early_Jomon Han"

# 8 本アウトグループ（順序は任意）
outgroups="Mbuti.DG Russia_Ust_Ishim Russia_Kostenki14 Russia_MA1_HG \
Papuan Karitiana Russia_DevilsCave_N China_Tianyuan"

###############################################################################
# (1) Sources だけ → qpWave① 用
###############################################################################
echo ${sources} | tr ' ' '\n' > left.sources.pops      # 1 行ずつ改行出力

###############################################################################
# (2) Target＋Sources → qpWave② & qpAdm 用
#     ── Target を必ず 1 行目に置く（qpAdm の仕様）
###############################################################################
echo ${target} ${sources} | tr ' ' '\n' > left.TS.pops

###############################################################################
# (3) 共通 Right (= Outgroups) ファイル
###############################################################################
echo ${outgroups} | tr ' ' '\n' > right.pops

###############################################################################
# ☆ 参考：実行例
# qpWave ①（Sources がクレードか）
#   qpWave -p parfile left=left.sources.pops right=right.pops > qpwave1.out
#
# qpWave ②（Target を加え rank が +1 になるか）
#   qpWave -p parfile left=left.TS.pops     right=right.pops > qpwave2.out
#
# qpAdm（混合比推定）
#   qpAdm  -p parfile left=left.TS.pops     right=right.pops > qpadm.out
###############################################################################
