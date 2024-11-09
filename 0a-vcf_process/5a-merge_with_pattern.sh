#!/bin/bash

# ここを変更して、マージ対象となるフォルダとファイル名を指定
bed_folder="for_PRS"  # フォルダ名を指定
file_name="jomon_for_PRS"  # 生成されるファイル名を指定
pattern=""  # 検索するファイルのワイルドカードパターンを指定

folder_path="/home1/mkato/hdd_data/1-merged-data/${bed_folder}"  # フォルダパスを指定
output_folder="$folder_path/merged"  # 出力先のフォルダを指定
mkdir -p $output_folder

cd $folder_path

# ワイルドカードパターンに一致するファイル群を探索し、.bimファイルに対応するベースファイルリストを作成
find "$folder_path" -type f -name "${pattern}*.bim" -print | while read file; do
    echo "${file%.*}"  # 拡張子'.bim'を省略して出力
done > output.txt  # リストをファイルにリダイレクト

echo "merge_list created"

# plinkのパス（/usr/local/bin/plink）が通っていないので通す
export PATH=$PATH:/usr/local/bin

# PLINKを使用してリストに基づきマージを試行
plink --merge-list output.txt --out "${folder_path}/m_${file_name}"

echo "merge trial done"

# missnpファイルが存在する場合、エラーポジションを除外して再度マージを試行
if test -e "${folder_path}/m_${file_name}.missnp"; then
    echo "missnp is found, attempting to exclude problematic SNPs"
    while read line; do
        plink --make-bed --exclude "${folder_path}/m_${file_name}.missnp" --bfile $line --chr 1-22 --out "${line}.tmp"
    done < output.txt
    echo "missnp has been excluded"
fi

# 一時ファイルリストを作成し、再度マージを実行
while read line; do
    echo "$line.tmp" >> "output.tmp.txt"
done < output.txt

plink --merge-list output.tmp.txt --out "${folder_path}/m_${file_name}"

# 不要な一時ファイルの削除
rm output.txt
rm output.tmp.txt
rm "${folder_path}/m_${file_name}.missnp"
find "$folder_path" -name "*tmp*" -type f -delete

# 最終生成物を出力フォルダへ移動
mv ${folder_path}/m_* $output_folder

echo "Merge process completed and files moved to $output_folder"
