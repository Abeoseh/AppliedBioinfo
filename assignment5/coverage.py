import pandas as pd
from matplotlib import pyplot as plt
df = pd.read_csv("ERR15846824/bam//aligned_coordinates.txt", names = ["chr","pos"], dtype={"pos":str},sep = "\t")
df = df[df.chr != "*"]
counts = df.pos.value_counts().to_dict()
plt.figure(figsize=(11, 6))
plt.bar(counts.keys(), counts.values())
plt.xticks(rotation=90)
plt.savefig("./images/coverage_uniform.png")

print(f"There are {len(counts)} positions with a max coverage of {max(counts.values())} and a min coverage of {min(counts.values())}")
print(counts)