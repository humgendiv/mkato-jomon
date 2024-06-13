import re
import gzip
import os
from concurrent.futures import ProcessPoolExecutor

def process_vcf(input_file, output_file):
    with gzip.open(input_file, 'rt') as infile, gzip.open(output_file, 'wt') as outfile:
        for line in infile:
            if line.startswith('#'):
                if line.startswith('##contig') or line.startswith('#CHROM'):
                    line = re.sub(r'chr(\d+)', r'\1', line)
                outfile.write(line)
            else:
                fields = line.strip().split('\t')
                chrom = fields[0]
                pos = fields[1]
                alt = fields[4]
                info = fields[7]
                format_info = fields[8]
                sample_info = fields[9]

                # Remove 'chr' prefix from CHROM field
                fields[0] = re.sub(r'^chr', '', chrom)

                # Remove ',<NON_REF>' from ALT field and replace '<NON_REF>' with '.'
                fields[4] = re.sub(r',<NON_REF>', '', alt)
                fields[4] = re.sub(r'^<NON_REF>$', '.', fields[4])

                # Find the index of DP and GT in FORMAT field
                format_fields = format_info.split(':')
                dp_index = format_fields.index('DP') if 'DP' in format_fields else -1
                gt_index = format_fields.index('GT') if 'GT' in format_fields else -1

                # Check if DP is less than 10 or GT is './.'
                if dp_index != -1 and gt_index != -1:
                    sample_fields = sample_info.split(':')
                    depth = int(sample_fields[dp_index])
                    genotype = sample_fields[gt_index]

                    if depth >= 10 and genotype != './.':
                        # Set ID field as CHROM:POS
                        fields[2] = f"{fields[0]}:{pos}"
                        
                        # Expand END information
                        end_match = re.search(r'END=(\d+)', info)
                        if end_match:
                            end_pos = int(end_match.group(1))
                            for new_pos in range(int(pos) + 1, end_pos + 1):
                                new_fields = fields.copy()
                                new_fields[1] = str(new_pos)
                                new_fields[2] = f"{fields[0]}:{new_pos}"
                                new_fields[3] = '.'
                                outfile.write('\t'.join(new_fields) + '\n')
                        else:
                            outfile.write('\t'.join(fields) + '\n')

# Set input and output file paths
#input_dir = '/home/mkato/hdd_data/data/0-0-raw_vcf'
#output_dir = '/home/mkato/hdd_data/data/0-0-raw_vcf/complete'
input_dir = '/home/mkato/hdd_data/data/0-0-raw_vcf/new_comp/'
output_dir = '/home/mkato/hdd_data/data/0-0-raw_vcf/new_comp/00-filter_makeid_exchr'
# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get the list of VCF files in the input directory
vcf_files = [filename for filename in os.listdir(input_dir) if filename.endswith('.vcf.gz')]

# Create a process pool executor
with ProcessPoolExecutor() as executor:
    # Submit tasks to process each VCF file
    futures = []
    for filename in vcf_files:
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, filename)
        future = executor.submit(process_vcf, input_file, output_file)
        futures.append(future)

    # Wait for all tasks to complete
    for future in futures:
        future.result()
