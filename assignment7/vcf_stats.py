import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


print("""
    #########################
    ####### VCF Stats #######
    #########################
""")

df = pd.read_csv("ERR15846824/vcf/ERR15846824.vcf", skiprows=36, sep="\t")

print(f"Chromosomes with variants: {df["#CHROM"].unique().tolist()}")



subs = df['REF'].astype(str) + '-' + df['ALT'].astype(str)
sub_dict = {}
for sub in subs:
    if sub not in sub_dict: sub_dict[sub] = 1
    else: sub_dict[sub] += 1

print("Reference-Sample SNP substitution count:")
print(sub_dict)


plt.hist(df.POS)
plt.ticklabel_format(style='plain', axis='both')
plt.xlabel('Variant Position')
plt.ylabel('Frequency')
plt.title('Frequency of variant positions')
plt.savefig("images/vcf_stats.png")