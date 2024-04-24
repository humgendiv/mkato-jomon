if [ $# -eq 0 ]; then
    echo "Please provide a directory path as an argument"
    exit 1
fi

input_dir=$1

for bim_file in "$input_dir"/*.bim; do
    if [ -e "$bim_file" ]; then
	temp_file=$(mktemp)
	awk 'BEGIN {OFS="\t"} {$2 = $1 ":" $4; print}' "$bim_file" > "$temp_file"
	mv "$temp_file" "$bim_file"
	echo "Updated $bim_file"

    fi
done

echo "Done. All Bim files in $input_dir have been updated"
