#!/bin/bash

#!ここを変える！(基本的にbedフォルダ内にすること)
bed_folder="0-3-extract_plink"
folder_path="/home1/mkato/hdd_data/data/${bed_folder}" # フォルダのパスを指定する

cd $folder_path

for file in $(find "$folder_path" -type f -name "*.bim" -print); do
    echo "${file%.*}" # 拡張子'.bim'を省略して出力する
done > output.txt # 出力をファイルにリダイレクトする
echo "merge_list created"

plink --merge-list output.txt --out "${folder_path}/m_${bed_folder}"

echo "merge trial done"

if test -e "${folder_path}/m_${bed_folder}.missnp"; then
    echo "missnp is found"
    while read line; do
        plink --make-bed --exclude "${folder_path}/m_${bed_folder}.missnp" --bfile $line --chr 1-22 --out "${line}.tmp"
    done < output.txt
    echo "missnp has excluded"
fi

while read line; do
    echo "$line.tmp" >> "output.tmp.txt"
done < output.txt

plink --merge-list output.tmp.txt --out "${folder_path}/m_${bed_folder}"

rm output.txt
rm output.tmp.txt
rm "${folder_path}/m_${bed_folder}.missnp"
find "$folder_path" -name "*tmp*" -type f -delete
mkdir -p ../0-4-merge_and_convert
mv ${folder_path}/m_* ../0-4-merge_and_convert/
