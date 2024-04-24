def read_snp_positions(file_path):
    with open(file_path, 'r') as file:
        return set(line.strip() for line in file)

bim_file = "/home/mkato/hdd_data/data/bim/1240K.bim"
array_id_file = "/home/mkato/hdd_data/data/bim/array_ID_ken.txt"
unique_snps_file = "/home/mkato/hdd_data/data/PS/unique_snps.txt"

bim_snps = read_snp_positions(bim_file)
array_id_snps = read_snp_positions(array_id_file)
unique_snps = read_snp_positions(unique_snps_file)

not_in_bim = unique_snps - bim_snps
not_in_array_id = unique_snps - array_id_snps

print("unique_snps.txtにあって1240K.bimにないSNP位置の数:", len(not_in_bim))
print("unique_snps.txtにあってarray_ID_ken.txtにないSNP位置の数:", len(not_in_array_id))
