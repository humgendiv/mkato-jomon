# CHR変数は、処理する染色体番号を設定します。ここでは1から22までを指定する必要があります。
for CHR in {1..22}
do
    qsub -v CHR=$CHR 5-3-23.sh
done