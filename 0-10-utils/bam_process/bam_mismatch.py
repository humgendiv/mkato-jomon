bam_file = "/home/mkato/hdd_data/data/bam/share/Todo5_Dra.bam"



import pysam

def count_reads_with_high_mismatches(bam_file, mismatch_threshold, batch_size=1000000):
    high_mismatch_count = 0
    total_read_count = 0

    with pysam.AlignmentFile(bam_file, "rb") as bamfile:
        for i, read in enumerate(bamfile):
            total_read_count += 1
            if read.has_tag("NM"):
                nm_tag = read.get_tag("NM")
                if nm_tag > mismatch_threshold:
                    high_mismatch_count += 1

            if (i + 1) % batch_size == 0:
                print(f"Processed {i + 1} reads.")
                print(f"Reads with more than {mismatch_threshold} mismatches: {high_mismatch_count}")
                print(f"Total reads: {total_read_count}")
                print(f"Percentage of reads with high mismatches: {high_mismatch_count / total_read_count * 100:.2f}%")
                print("---")

    return high_mismatch_count, total_read_count

# BAMファイルのパスとミスマッチのしきい値を指定
mismatch_threshold = 5

# ミスマッチが多すぎるリードの数を数える
high_mismatch_count, total_read_count = count_reads_with_high_mismatches(bam_file, mismatch_threshold)

# 最終結果を表示
print("Final Results:")
print(f"Reads with more than {mismatch_threshold} mismatches: {high_mismatch_count}")
print(f"Total reads: {total_read_count}")
print(f"Percentage of reads with high mismatches: {high_mismatch_count / total_read_count * 100:.2f}%")
