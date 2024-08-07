#bamファイルが格納されているディレクトリを予め指定しておく
DATADIR=/home1/mkato/hdd_data/data/bam/share/Iyai1/
#DATADIR=/home/mkato/hdd_data/data/fastq/FM027/bam/

# bamファイルを指定. ファイル名はこのスクリプトの実行時に第1引数として拡張子付きで指定すること。
BAMFILE=${DATADIR}$1

echo "BAMFILE: $BAMFILE"
# BAMFILEの20番染色体に対して、デプスを計算する。
# DEPTHの小数点以下を切り捨てる
# Depthに関する情報。このスクリプトの実行時に第2引数として指定すること。

# まず、bamファイルの染色体に関する情報が、chrという文字列がつくかつかないかを判定する
# chrを除去するのは時間がかかるため、for文を回す際にchrつきに対応できるようにする。
# bamファイルの3列めの文字列にchrが含まれているかどうかを判定する。
# samtools viewでbamファイルを読み込み、awkで3列目の文字列を取得し、grepでchrを含むかどうかを判定する。
# samtoolsの結果に基づいて、chrを含むかどうかをchr_or_notに格納する。最初の行のみで十分。
chr_or_not=$(samtools view $BAMFILE | head -1 | cut -f 3 | grep -c "chr")
echo "chr_or_not: $chr_or_not"
# chr_or_notの値に応じて判定する
if [ $chr_or_not -eq 0 ]; then
	# このときchrは含まれていないので、通常のfor文で処理する
	echo "chr is NOT included"	
	DEPTH=$(/usr/local/bin/samtools depth -r 20 $BAMFILE | awk '{sum += $3} END {print sum / NR}')
        DEPTH=$(echo $DEPTH | awk -F. '{print $1}')
        echo "DEPTH: $DEPTH"
	for i in {1..22}
	do
		qsub -v BAMFILE=$BAMFILE,DEPTH=$DEPTH,CHROM=$i ./2a-sub-bamcaller.sh
	done
else
	# このときchrは含まれているので、for文の添字にchrをつけて処理する
	echo "chr is included"
	DEPTH=$(/usr/local/bin/samtools depth -r chr20 $BAMFILE | awk '{sum += $3} END {print sum / NR}')
        DEPTH=$(echo $DEPTH | awk -F. '{print $1}')
        echo "DEPTH: $DEPTH"

	for i in {1..22}
	do
		qsub -v BAMFILE=$BAMFILE,DEPTH=$DEPTH,CHROM=chr$i ./2a-sub-bamcaller.sh
	done
fi
