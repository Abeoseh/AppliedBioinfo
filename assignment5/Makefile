SHELL := /bin/sh

## Reference genome URL
GENOME_URL := https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/009/045/GCF_000009045.1_ASM904v1/GCF_000009045.1_ASM904v1_genomic.fna.gz

## Get sample from a bioproject
SRR_ID := ERR15846824
N := 35130
REF_GENOME := ref_genome/GCF_000009045.1_ASM904v1_genomic.fna
FASTQ1 := $(SRR_ID)/fastq/ERR15846824_1.fastq
FASTQ2 := $(SRR_ID)/fastq/ERR15846824_2.fastq



## create BAM name and index
BAM_FILE = $(SRR_ID)/bam/$(SRR_ID).bam
INDEX_PREFIX = $(SRR_ID)/index/$(SRR_ID)

.PHONY: all GENOME FASTQs INDEX ALIGN COVERAGE

all: GENOME FASTQs INDEX ALIGN COVERAGE


GENOME:
	## dir is similar to bash's basename so it extracts the directory
	mkdir -p $(dir $(REF_GENOME))
	curl -fsSL $(GENOME_URL) | gunzip > $(REF_GENOME)
	
	echo ""
	echo "Genome stats for Bacillus subtilis subsp. subtilis str. 168 "
	seqkit stats $(REF_GENOME)
	echo "==================================================================="


FASTQs:
	mkdir -p $(SRR_ID)/fastq
	fastq-dump -X $(N) --split-files $(SRR_ID) --outdir $(SRR_ID)/fastq
	
	echo ""
	echo "Fastq stats for Bacillus subtilis subsp. subtilis str. 168 "
	seqkit stats $(FASTQ1) $(FASTQ2)
	echo "==================================================================="



INDEX:
	mkdir -p $(dir $(INDEX_PREFIX))	
	bwa index -a is -p $(INDEX_PREFIX) $(REF_GENOME) 


ALIGN:
	mkdir -p $(dir $(BAM_FILE))
	bwa mem $(INDEX_PREFIX) $(FASTQ1) $(FASTQ2) | samtools sort -o $(BAM_FILE)
	samtools index $(BAM_FILE)
	echo "Alignment stats for Bacillus subtilis subsp. subtilis str. 168 "
	samtools flagstat $(BAM_FILE)
	echo "==================================================================="
	## info on the alignment coordinates
	samtools view $(BAM_FILE) | cut -f 3,4 > $(dir $(BAM_FILE))/aligned_coordinates.txt

	

COVERAGE:
	mkdir -p images
	python coverage.py
