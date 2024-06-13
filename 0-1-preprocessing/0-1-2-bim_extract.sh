DIR=/home1/mkato/hdd_data/data
#input_dir=${DIR}/0-0-raw_vcf/complete/plink_common
input_dir=${DIR}/0-0-raw_vcf/new_comp/01-tabix-split-toplink/plink
output_dir=/home1/mkato/hdd_data/data/0-3-extract_plink
extract_file=/home1/mkato/hdd_data/data/bim/1240K.bim
mkdir -p ${output_dir}
export PATH=/usr/local/bin:$PATH

#plink --make-bed --extract ${extract_file} --bfile ${input_dir}/${SAMPLE} --out ${output_dir}/${SAMPLE}


for bed_file in "$input_dir"/*.bed; do
    if [ -e "$bed_file" ]; then
	base_name=$(basename "$bed_file" .bed)
	plink --bfile "$input_dir"/"$base_name" --extract "$extract_file" --make-bed --out "$output_dir"/"$base_name"
	echo "Extracted SNPs from $bed_file"
    fi
done

echo "Done. Output files are in $output_dir"


