DIR=/home1/mkato/hdd_data/data
input_dir=${DIR}/0-0-raw_vcf/complete/plink_common
output_dir=${DIR}/Genomes/korean/jomon_korean_comm
extract_file=${DIR}/bim/jomon_korean_comm.txt
mkdir -p ${output_dir}
export PATH=/usr/local/bin:$PATH

plink --make-bed --extract ${extract_file} --bfile ${input_dir}/${SAMPLE} --out ${output_dir}/${SAMPLE}


for bed_file in "$input_dir"/*.bed; do
    if [ -e "$bed_file" ]; then
	base_name=$(basename "$bed_file" .bed)
	plink --bfile "$input_dir"/"$base_name" --extract "$extract_file" --make-bed --out "$output_dir"/"$base_name"
	echo "Extracted SNPs from $bed_file"
    fi
done

echo "Done. Output files are in $output_dir"


