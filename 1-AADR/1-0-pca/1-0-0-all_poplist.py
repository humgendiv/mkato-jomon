import yaml

# Load the configuration file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

ind_file_path = config['file_paths']['input_ind']

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
all_poplist_path = config['file_paths']['output_allpop']
with open(all_poplist_path, 'w') as f:
    for population in sorted_unique_populations:
        f.write(f"{population}\n")
