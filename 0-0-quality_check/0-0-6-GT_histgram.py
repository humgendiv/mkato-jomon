import gzip
import matplotlib
matplotlib.use('Agg')  # コンソールで実行するためのバックエンドを設定
import matplotlib.pyplot as plt

def plot_depth_and_mq_histograms(vcf_file, output_file):
    dp_homo_ref = []
    dp_hetero = []
    dp_homo_alt = []
    mq_homo_ref = []
    mq_hetero = []
    mq_homo_alt = []

    with gzip.open(vcf_file, 'rt') if vcf_file.endswith('.gz') else open(vcf_file, 'r') as file:
        for line in file:
            if line.startswith('#'):
                continue
            fields = line.strip().split('\t')
            info = dict(item.split('=') for item in fields[7].split(';') if '=' in item)
            format_fields = fields[8].split(':')
            sample_fields = fields[9].split(':')

            try:
                dp_index = format_fields.index('DP')
                sample_dp = int(sample_fields[dp_index])
            except ValueError:
                continue  # DPフィールドがない場合はスキップ

            mq = float(info.get('MQ', 0))  # MQが存在しない場合は0を使用

            gt_index = format_fields.index('GT')
            sample_gt = sample_fields[gt_index]

            if sample_gt == '0/0':
                dp_homo_ref.append(sample_dp)
                mq_homo_ref.append(mq)
            elif sample_gt in ['0/1', '1/0']:
                dp_hetero.append(sample_dp)
                mq_hetero.append(mq)
            elif sample_gt == '1/1':
                dp_homo_alt.append(sample_dp)
                mq_homo_alt.append(mq)

    fig, axs = plt.subplots(2, 3, figsize=(15, 8))
    axs[0, 0].hist(dp_homo_ref, bins=50)
    axs[0, 0].set_title('Depth (0/0)')
    axs[0, 1].hist(dp_hetero, bins=50)
    axs[0, 1].set_title('Depth (0/1 or 1/0)')
    axs[0, 2].hist(dp_homo_alt, bins=50)
    axs[0, 2].set_title('Depth (1/1)')
    axs[1, 0].hist(mq_homo_ref, bins=50)
    axs[1, 0].set_title('Mapping Quality (0/0)')
    axs[1, 1].hist(mq_hetero, bins=50)
    axs[1, 1].set_title('Mapping Quality (0/1 or 1/0)')
    axs[1, 2].hist(mq_homo_alt, bins=50)
    axs[1, 2].set_title('Mapping Quality (1/1)')

    plt.tight_layout()
    plt.savefig(output_file)


sample='FM020'
plot_depth_and_mq_histograms(f'/home/mkato/hdd_data/data/0-0-raw_vcf/new_comp/{sample}.vcf.gz', f'./{sample}.png')
