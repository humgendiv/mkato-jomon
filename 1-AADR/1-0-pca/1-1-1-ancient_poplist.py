import yaml 

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# 結局手動でやったので頑張ってください。


ind_file_path = config['file_paths']['input_ind'] # Path to the input .ind file

# Define the list of 1000 Genomes Project population codes and the special cases
target_pop_codes = [
    "CHB", "JPT", "CHS", "CDX", "KHV", "CHD",
]
special_cases = ["Control", "Japan", "China", "Korea"]

# Initialize an empty set to store the selected populations
selected_populations = set()

# Read the file line by line and filter populations based on the criteria
with open(ind_file_path, 'r') as f:
    for line in f:
        fields = line.strip().split()
        if len(fields) >= 3:
            pop = fields[2]
            # Check if it's a special case
            if any(pop.startswith(special) for special in special_cases):
                selected_populations.add(pop)
                continue
            # Check if it's a 1000 Genomes Project sample with .DG or .SG suffix
            if any(pop.startswith(code + ".DG") or pop.startswith(code + ".SG") for code in target_pop_codes):
                selected_populations.add(pop)

# Sort the selected populations for better readability
sorted_selected_populations = sorted(list(selected_populations))

# Write these selected populations to a new poplist file
selected_poplist_path = config['file_paths']['output_ancientpop'] # Path to the output selected poplist file
with open(selected_poplist_path, 'w') as f:
    for population in sorted_selected_populations:
        f.write(f"{population}\n")

