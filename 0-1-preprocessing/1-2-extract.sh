if [ $# -eq 0 ]; then
    echo "Please provide a directory path as an argument"
    exit 1
fi

input_dir=$1
extract_file="/home/mkato/hdd_data/data/bim/merged_positions.bim"

output_dir="$input_dir"_extracted
mkdir -p "$output_dir"

for bed_file in "$input_dir"/*.bed; do
    if [ -e "$bed_file" ]; then
	base_name=$(basename "$bed_file" .bed)
	plink --bfile "$input_dir"/"$base_name" --extract "$extract_file" --make-bed --out "$output_dir"/"$base_name"_extracted
	echo "Extracted SNPs from $bed_file"
    fi
done

echo "Done. Output files are in $output_dir"
