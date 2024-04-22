ind_file_path = '/home1/mkato/hdd_data/data/1-withAADR/1-0-merged_eigen/jomon_aadr.ind'

# Extract the unique population names from the 3rd column and write them to a file named "all_poplist.txt"
unique_populations = set()

# Read the file line by line to extract unique population names
with open(ind_file_path, 'r') as f:
    for line in f:
        fields = line.strip().split()
        if len(fields) >= 3:
            unique_populations.add(fields[2])

# Sort the unique populations for better readability
sorted_unique_populations = sorted(list(unique_populations))

# Write these unique populations to "all_poplist.txt"
all_poplist_path = '/home1/mkato/hdd_data/data/1-withAADR/1-0-merged_eigen/all_poplist.txt'
with open(all_poplist_path, 'w') as f:
    for population in sorted_unique_populations:
        f.write(f"{population}\n")
