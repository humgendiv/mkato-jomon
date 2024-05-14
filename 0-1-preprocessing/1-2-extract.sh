#input_dir="/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink_common"
input_dir="/home/mkato/hdd_data/data/Genomes1000/jptvcf_bed/merged"
#extract_file="/home/mkato/hdd_data/data/bim/merged_positions.bim"
#extract_file="/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink/common_snps.txt"
extract_file="/home/mkato/hdd_data/data/bim/jpt_full.txt"
#output_dir="$input_dir"_extracted
output_dir="$input_dir"/extracted
mkdir -p "$output_dir"

for bed_file in "$input_dir"/*.bed; do
    if [ -e "$bed_file" ]; then
	base_name=$(basename "$bed_file" .bed)
	/usr/local/bin/plink --bfile "$input_dir"/"$base_name" --extract "$extract_file" --make-bed --out "$output_dir"/"$base_name"_extracted
	echo "Extracted SNPs from $bed_file"
    fi
done

echo "Done. Output files are in $output_dir"
