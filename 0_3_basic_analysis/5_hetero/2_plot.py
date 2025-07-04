# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

het_data = pd.read_csv('plink2.het', sep='\t')

# Calculate heterozygous site ratio
het_data['hetero_ratio'] = (het_data['OBS_CT'] - het_data['O(HOM)']) / het_data['OBS_CT']

plt.figure(figsize=(12, 8))
markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', '*', 'h', 'H', '+', 'x', '8', 'd', '|', '_', '.', ',', '1', '2', '3', '4']
for i, pop in enumerate(het_data['#FID'].unique()):
    pop_data = het_data[het_data['#FID'] == pop]
    marker = markers[i % len(markers)]
    plt.scatter(pop_data['OBS_CT'], pop_data['hetero_ratio'], alpha=0.6, label=pop, marker=marker, s=50)

plt.xlabel('OBS_CT (Observed Count)')
plt.ylabel('Heterozygous Site Ratio')
plt.title('Heterozygous Site Ratio vs OBS_CT Scatter Plot by Population')
plt.grid(True, alpha=0.3)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.savefig('F_vs_OBS_CT_scatter.png', dpi=300, bbox_inches='tight')
plt.show()