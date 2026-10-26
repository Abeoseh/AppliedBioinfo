SHELL := /bin/sh

## Reference genome URL
GENOME_URL ?= https://ftp.ensemblgenomes.ebi.ac.uk/pub/bacteria/release-63/fasta/bacteria_0_collection/bacillus_subtilis_subsp_subtilis_str_168_gca_000009045/dna/Bacillus_subtilis_subsp_subtilis_str_168_gca_000009045.ASM904v1.dna.toplevel.fa.gz

## Reference annotation URL
ANNOTATION_URL ?= https://ftp.ensemblgenomes.ebi.ac.uk/pub/bacteria/release-63/gff3/bacteria_0_collection/bacillus_subtilis_subsp_subtilis_str_168_gca_000009045/Bacillus_subtilis_subsp_subtilis_str_168_gca_000009045.ASM904v1.63.gff3.gz

## Get sample from a bioproject
SRR_ID ?= ERR15846824
N ?= 32655

REF_FILE ?= Bacillus_subtilis_subsp_subtilis_str_168_gca_000009045.ASM904v1.dna.toplevel.fa
ANN_FILE ?= Bacillus_subtilis_subsp_subtilis_str_168_gca_000009045.ASM904v1.63.gff3

REF_GENOME := $(SRR_ID)/ref_genome/$(REF_FILE)
REF_ANNOTATION := $(SRR_ID)/ref_genome/$(ANN_FILE)
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

	curl -fsSL $(ANNOTATION_URL) | gunzip > $(REF_ANNOTATION)
	
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
	bcftools call --ploidy 1 --annotate 'FORMAT/GQ' -mv -O u | \
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


	# Add consequence annotations to the VCF
	bcftools csq \
		-p a \
		-f $(REF_GENOME) \
		-g $(REF_ANNOTATION) \
		-O z -W \
		-o merged_vcf/merged-VCF.csq.vcf.gz \
		merged_vcf/merged-VCF.vcf.gz


	# Write one consequence per row
	bcftools +split-vep merged_vcf/merged-VCF.csq.vcf.gz \
    		-a BCSQ -d -H \
		-f '%CHROM\t%POS\t%REF\t%ALT\t%Consequence\t%gene\t%transcript\t%biotype\t%strand\t%amino_acid_change\t%dna_change\n' \
		> merged_vcf/annotations.txt

	