if [ $# -eq 0 ]; then
    echo "Please provide a directory path as an argument"
    exit 1
fi

input_dir=$1
output_dir="$input_dir"_bed
mkdir -p "$output_dir"

for vcf_file in "$input_dir"/*.vcf.gz; do
    if [ -e "$vcf_file" ]; then
	base_name=$(basename "$vcf_file" .vcf.gz)
	plink --vcf "$vcf_file" --make-bed --out "$output_dir"/"$base_name"
    fi
done

echo "Done. Output files are in $output_dir"
