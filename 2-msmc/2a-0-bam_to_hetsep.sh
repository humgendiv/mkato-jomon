#bamファイルが格納されているディレクトリを予め指定しておく
DATADIR=/home1/mkato/hdd_data/data/bam/share/
# bamファイルを指定. ファイル名はこのスクリプトの実行時に第1引数として拡張子付きで指定すること。
BAMFILE=${DATADIR}$1
# Depthに関する情報。このスクリプトの実行時に第2引数として指定すること。
DEPTH=$2

# まず、bamファイルの染色体に関する情報が、chrという文字列がつくかつかないかを判定する
# chrを除去するのは時間がかかるため、for文を回す際にchrつきに対応できるようにする。
# bamファイルの3列めの文字列にchrが含まれているかどうかを判定する。
# samtools viewでbamファイルを読み込み、awkで3列目の文字列を取得し、grepでchrを含むかどうかを判定する。

chr_or_not = samtools view $BAMFILE | head | awk '{print $3}' | grep -q "chr"
if [ $chr_or_not -eq 0 ]; then
	# このときchrは含まれていないので、通常のfor文で処理する
	for i in {1..22}
	do
		qsub -v BAMFILE=$BAMFILE,DEPTH=$DEPTH,CHR=$i ./2a-sub-bamcaller.sh
	done
else
	# このときchrは含まれているので、for文の添字にchrをつけて処理する
	for i in {1..22}
	do
		qsub -v BAMFILE=$BAMFILE,DEPTH=$DEPTH,CHR=chr$i ./2a-sub-bamcaller.sh
	done
fi
