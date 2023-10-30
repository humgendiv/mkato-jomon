# Importing the required libraries
import gzip

def calculate_homozygosity_density(vcf_gz_file_path):
    """
    Calculates the density of homozygous sites from a VCF.gz file.
    
    Parameters:
        vcf_gz_file_path (str): Path to the input VCF.gz file.
        
    Returns:
        float: Density of homozygous sites.
    """
    
    # Initialize counters for total sites and homozygous sites
    total_sites = 0
    homozygous_sites = 0
    
    # Open the VCF.gz file for reading
    with gzip.open(vcf_gz_file_path, 'rt') as f:
        for line in f:
            # Skip header lines
            if line.startswith('#'):
                continue
            
            # Increment the total site counter
            #total_sites += 1
            
            # Split the line into its columns
            columns = line.strip().split('\t')
            
            # Extract the genotype information (assuming it's in the 10th column)
            # Format is usually GT:AD:DP:GQ:PL -> e.g., 0/1:3,8:11:99:123,0,98
            genotype_info = columns[9]
            
            # Extract the genotype (GT) field (assuming it's the first field in the genotype column)
            genotype = genotype_info.split(':')[0]
            
            # Check if the site is homozygous
            if genotype == '1/1':
                
                homozygous_sites += 1
            elif genotype == '1/0' or genotype == '0/1':
                total_sites += 1
            else:

    
    # Calculate the density of homozygous sites
    if total_sites == 0:
        return 0  # Avoid division by zero
    
    homozygosity_density = homozygous_sites / total_sites
    
    result = [homozygous_sites, total_sites, ]
    return 

# Dummy VCF.gz file path (This is just a placeholder as I cannot access external files)
# You can replace this with the path to your actual VCF.gz file
sample = "FM020"
vcf_gz_file_path = f"/home/mkato/hdd_data/data/0-1-filtered_vcf/{sample}_filtered2.vcf.gz"

# Uncomment the below line to actually run the function with your VCF.gz file
result = calculate_homozygosity_density(vcf_gz_file_path)
print(result)