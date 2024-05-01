input_dir="/home/mkato/hdd_data/data/0-3-extract_plink"
#extract_file="/home/mkato/hdd_data/data/bim/merged_positions.bim"
extract_file="/home/mkato/hdd_data/data/bim/1240K_downsized_jomon.bim"
#output_dir="$input_dir"_extracted
output_dir="$input_dir"_downsized_jomon
mkdir -p "$output_dir"

for bed_file in "$input_dir"/*.bed; do
    if [ -e "$bed_file" ]; then
	base_name=$(basename "$bed_file" .bed)
	plink --bfile "$input_dir"/"$base_name" --extract "$extract_file" --make-bed --out "$output_dir"/"$base_name"_extracted
	echo "Extracted SNPs from $bed_file"
    fi
done

echo "Done. Output files are in $output_dir"
