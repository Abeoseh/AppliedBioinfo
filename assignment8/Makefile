SHELL := /bin/sh

## Reference genome URL
GENOME_URL ?= https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/015/785/GCF_000015785.2_ASM1578v2/GCF_000015785.2_ASM1578v2_genomic.fna.gz

## Get sample from a bioproject
SRR_ID ?= ERR15846824
N ?= 32655

REF_FILE ?= GCF_000015785.2_ASM1578v2_genomic.fna
REF_GENOME := $(SRR_ID)/ref_genome/$(REF_FILE)
FASTQ1 := $(SRR_ID)/fastq/$(SRR_ID)_1.fastq
FASTQ2 := $(SRR_ID)/fastq/$(SRR_ID)_2.fastq



## create BAM name and index
BAM_FILE = $(SRR_ID)/bam/$(SRR_ID).bam
INDEX_PREFIX = $(SRR_ID)/index/$(SRR_ID)




## create vcf folder


.PHONY: all GENOME FASTQs INDEX ALIGN VARIANTS MERGE_VARIANTS

## run using make MERGE=1 to merge the VCF files
ifdef MERGE
all: GENOME FASTQs INDEX ALIGN VARIANTS MERGE_VARIANTS
else
all: GENOME FASTQs INDEX ALIGN VARIANTS
endif

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

VARIANTS:
	mkdir -p $(SRR_ID)/vcf
	bcftools mpileup -d 50 --annotate 'INFO/AD,FORMAT/DP,FORMAT/AD,FORMAT/ADF,FORMAT/ADR,FORMAT/SP' \
	-O u -f $(REF_GENOME) $(BAM_FILE) | \
	bcftools call --ploidy 2 --annotate 'FORMAT/GQ' -mv -O u | \
	bcftools norm -f $(REF_GENOME) -d all -O u | \
	bcftools sort --write-index -O z -o $(SRR_ID)/vcf/$(SRR_ID).vcf.gz

	ls -lh $(SRR_ID)/vcf/$(SRR_ID).vcf.gz
	gunzip -kf $(SRR_ID)/vcf/$(SRR_ID).vcf.gz
	
	mkdir -p images
	python vcf_stats.py $(SRR_ID)

MERGE_VARIANTS:
	
	mkdir -p merged_vcf
	find . -name '*.vcf.gz' -not -path './merged_vcf/*' -print
	bcftools merge --write-index -O z \
		-o merged_vcf/merged-VCF.vcf.gz \
		$$(find . -name '*.vcf.gz' -not -path './merged_vcf/*')
	gunzip -kf merged_vcf/merged-VCF.vcf.gz
