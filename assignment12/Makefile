DATA_DIR := gene_level_count_matrix

.PHONY: help data quantify matrices all clean

help:
	@echo "make data        Download the tutorial reference and FASTQ data"
	@echo "make quantify    Build the Salmon index and quantify every sample"
	@echo "make matrices    Generate transcript- and gene-level count matrices"
	@echo "make all         Run data, quantification, and matrix generation"
	@echo "make clean       Remove generated matrices (not quantification inputs)"

data:
	$(MAKE) -C $(DATA_DIR) data

quantify: data
	$(MAKE) -C $(DATA_DIR) batch

matrices: quantify
	Rscript src/combine_transcript_counts.r
	Rscript src/combine_gene_counts.r

all: matrices

clean:
	rm -f results/transcript_counts.csv results/gene_counts.csv
