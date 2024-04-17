sample=${1}

data_dir=/home/mkato/hdd_data/data/0-0-raw_vcf

# data_dir内の$sample.g.vcf.gzというファイルに対して、
# 以下の処理を実行する
# 1. 染色体番号がchr1, chr2 ...となっているのを1, 2 ...に変更
# 2. ALT列に",<NON_REF>"という文字列が含まれている場合、それを削除
# 3. ALT列に"<NON_REF>"という文字列が含まれている場合、ピリオド"."に置換
# 4. 
