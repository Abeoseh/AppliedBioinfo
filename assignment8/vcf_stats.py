import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sys import argv

print("""
    #########################
    ####### VCF Stats #######
    #########################
""")

df = pd.read_csv(f"{argv[1]}/vcf/{argv[1]}.vcf", skiprows=36, sep="\t")

print(f"Chromosomes with variants: {df["#CHROM"].unique().tolist()}")



subs = df['REF'].astype(str) + '-' + df['ALT'].astype(str)
sub_dict = {}
for sub in subs:
    if sub not in sub_dict: sub_dict[sub] = 1
    else: sub_dict[sub] += 1

print("Reference-Sample SNP substitution count:")
print(sub_dict)


plt.hist(df.POS)
# plt.ticklabel_format(style='plain', axis='both')
# plt.xticks(rotation=30)
plt.xlabel('Variant Position')
plt.ylabel('Frequency')
plt.title(f'Frequency of variant positions for {argv[1]}')
plt.savefig(f"images/vcf_stats_{argv[1]}.png")