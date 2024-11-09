#!/bin/bash

#!ここを変える！(基本的にbedフォルダ内にすること)
bed_folder="for_PRS" # フォルダ名を指定する
file_name="jomons_for_PRS" # 生成ファイル名を指定する

folder_path="/home1/mkato/hdd_data/1-merged_data/${bed_folder}" # フォルダのパスを指定する
output_folder="$folder_path/merged" # 出力先のフォルダを指定する
#ここまで

mkdir -p $output_folder

cd $folder_path

for file in $(find "$folder_path" -type f -name "*.bim" -print); do
    echo "${file%.*}" # 拡張子'.bim'を省略して出力する
done > output.txt # 出力をファイルにリダイレクトする
echo "merge_list created"

# plinkのパス（/usr/loca/bin/plink）が通っていないので通す
export PATH=$PATH:/usr/local/bin
plink --merge-list output.txt --out "${folder_path}/m_${file_name}"

echo "merge trial done"

if test -e "${folder_path}/m_${file_name}.missnp"; then
    echo "missnp is found"
    while read line; do
        plink --make-bed --exclude "${folder_path}/m_${file_name}.missnp" --bfile $line --chr 1-22 --out "${line}.tmp"
    done < output.txt
    echo "missnp has excluded"
fi

while read line; do
    echo "$line.tmp" >> "output.tmp.txt"
done < output.txt

plink --merge-list output.tmp.txt --out "${folder_path}/m_${file_name}"

rm output.txt
rm output.tmp.txt
rm "${folder_path}/m_${file_name}.missnp"
find "$folder_path" -name "*tmp*" -type f -delete
mv ${folder_path}/m_* $output_folder 
