import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Set the input and output directories
input_dir = '/home/mkato/hdd_data/data/0-0-raw_vcf/complete/'
index_dir = '/home/mkato/hdd_data/data/0-0-raw_vcf/complete/'
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
    print(f"indexing: {filename}")
    # もし既にindexファイルがあれば、この工程はスキップする
    if os.path.exists(index_file):
        print(f"index file already exists: {index_file}")
    else:
        subprocess.run(['tabix', '-p', 'vcf', input_file])
    
    # Split by chromosome groups
    chrom_groups = ['1-7', '8-22']
    for group in chrom_groups:
        chrom_file = os.path.join(split_dir, f"{filename.replace('.vcf.gz', '')}.chr{group}.vcf.gz")
        print(f"splitting: {filename} -> {chrom_file}")
        if group == '1-7':
            region = '1,2,3,4,5,6,7'
        elif group == '8-22':
            region = '8,9,10,11,12,13,14,15,16,17,18,19,20,21,22'
        subprocess.run(['bcftools', 'view', '-r', region, input_file, '-Oz', '-o', chrom_file])
        
        # Convert to plink format
        plink_prefix = os.path.join(plink_dir, f"{filename.replace('.vcf.gz', '')}.chr{group}")
        print(f"converting to plink: {chrom_file} -> {plink_prefix}")
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
