import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Set the input and output directories
input_dir = '/home/mkato/hdd_data/data/0-0-raw_vcf/complete'
index_dir = '/home/mkato/hdd_data/data/0-0-raw_vcf/complete/indexed'
split_dir = '/home/mkato/hdd_data/data/0-0-raw_vcf/complete/split'
plink_dir = '/home/mkato/hdd_data/data/0-0-raw_vcf/complete/plink'

# Create the output directories if they don't exist
os.makedirs(index_dir, exist_ok=True)
os.makedirs(split_dir, exist_ok=True)
os.makedirs(plink_dir, exist_ok=True)

# Get the list of VCF files in the input directory
vcf_files = [filename for filename in os.listdir(input_dir) if filename.endswith('.vcf.gz')]

def process_file(filename):
    # Create index file
    input_file = os.path.join(input_dir, filename)
    index_file = os.path.join(index_dir, filename + '.tbi')
    subprocess.run(['tabix', '-p', 'vcf', input_file])
    
    # Split by chromosome
    for chrom in range(1, 23):
        chrom_file = os.path.join(split_dir, f"{filename.replace('.g.vcf.gz', '')}.chr{chrom}.vcf.gz")
        subprocess.run(['bcftools', 'view', '-r', str(chrom), input_file, '-Oz', '-o', chrom_file])
        
        # Convert to plink format
        plink_prefix = os.path.join(plink_dir, f"{filename.replace('.g.vcf.gz', '')}.chr{chrom}")
        subprocess.run(['/usr/local/bin/plink', '--make-bed', '--allow-extra-chr', '--vcf', chrom_file, '--out', plink_prefix])

# Create a thread pool executor
with ThreadPoolExecutor() as executor:
    # Submit tasks to process each VCF file
    futures = []
    for filename in vcf_files:
        future = executor.submit(process_file, filename)
        futures.append(future)

    # Wait for all tasks to complete
    for future in futures:
        future.result()
