#☆ 参考：実行例
#qpWave ①（Sources がクレードか）
/home/mkato/Repo/AdmixTools/bin/qpWave -p ./1p_qpWave1.par > qpwave1.out

#qpWave ②（Target を加え rank が +1 になるか）
/home/mkato/Repo/AdmixTools/bin/qpWave -p ./1p_qpWave2.par > qpwave2.out

#qpAdm（混合比推定）
/home/mkato/Repo/AdmixTools/bin/qpAdm  -p ./1p_qpAdm.par > qpadm.out
# ###############################################################################