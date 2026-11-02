SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c
.DELETE_ON_ERROR:

## Reference genome and annotation
GENOME_URL ?= https://ftp.ensemblgenomes.ebi.ac.uk/pub/bacteria/release-63/fasta/bacteria_0_collection/bacillus_subtilis_subsp_subtilis_str_168_gca_000009045/dna/Bacillus_subtilis_subsp_subtilis_str_168_gca_000009045.ASM904v1.dna.toplevel.fa.gz
ANNOTATION_URL ?= https://ftp.ensemblgenomes.ebi.ac.uk/pub/bacteria/release-63/gff3/bacteria_0_collection/bacillus_subtilis_subsp_subtilis_str_168_gca_000009045/Bacillus_subtilis_subsp_subtilis_str_168_gca_000009045.ASM904v1.63.gff3.gz
REF_FILE ?= Bacillus_subtilis_subsp_subtilis_str_168_gca_000009045.ASM904v1.dna.toplevel.fa
ANN_FILE ?= Bacillus_subtilis_subsp_subtilis_str_168_gca_000009045.ASM904v1.63.gff3
REF_GENOME := ref_genome/$(REF_FILE)
REF_ANNOTATION := ref_genome/$(ANN_FILE)
INDEX_PREFIX := ref_genome/index/bsubtilis168

## Per-run parameters (override on the make command line)
SRR_ID ?= ERR15846824
N ?= 140000
THREADS ?= 2
JOBS ?= 2
DESIGN ?= design.csv

FASTQ_DIR := $(SRR_ID)/fastq
FASTQ1 := $(FASTQ_DIR)/$(SRR_ID)_1.fastq
FASTQ2 := $(FASTQ_DIR)/$(SRR_ID)_2.fastq
FASTQ_STAMP := $(FASTQ_DIR)/.spots-$(N).complete
BAM_FILE := $(SRR_ID)/bam/$(SRR_ID).bam
VCF_FILE := $(SRR_ID)/vcf/$(SRR_ID).vcf.gz
SAMPLES := $(shell awk -F, 'NR > 1 && NF { print $$1 }' $(DESIGN))
VCF_FILES := $(foreach run,$(SAMPLES),$(run)/vcf/$(run).vcf.gz)

.PHONY: all GENOME FASTQs INDEX ALIGN VARIANTS batch MERGE_VARIANTS

all: GENOME $(VCF_FILE)

GENOME: $(REF_GENOME) $(REF_ANNOTATION)

$(REF_GENOME):
	mkdir -p $(@D)
	curl -fsSL $(GENOME_URL) | gzip -dc > $@.tmp
	mv $@.tmp $@

$(REF_ANNOTATION):
	mkdir -p $(@D)
	curl -fsSL $(ANNOTATION_URL) | gzip -dc > $@.tmp
	mv $@.tmp $@

FASTQs: $(FASTQ_STAMP)

$(FASTQ_STAMP):
	mkdir -p $(FASTQ_DIR)
	if [[ -s $(FASTQ1) && -s $(FASTQ2) && $$(( $$(wc -l < $(FASTQ1)) / 4 )) -eq $(N) && $$(( $$(wc -l < $(FASTQ2)) / 4 )) -eq $(N) ]]; then \
		touch $@; \
	else \
		rm -f $(FASTQ1) $(FASTQ2); \
		fastq-dump -X $(N) --split-files $(SRR_ID) --outdir $(FASTQ_DIR); \
		test -s $(FASTQ1) && test -s $(FASTQ2); \
		touch $@; \
	fi
	seqkit stats $(FASTQ1) $(FASTQ2)

INDEX: $(INDEX_PREFIX).bwt

$(INDEX_PREFIX).bwt: $(REF_GENOME)
	mkdir -p $(@D)
	bwa index -a is -p $(INDEX_PREFIX) $(REF_GENOME)

ALIGN: $(BAM_FILE) $(BAM_FILE).bai

$(BAM_FILE): Makefile $(FASTQ_STAMP) $(INDEX_PREFIX).bwt
	mkdir -p $(@D)
	bwa mem -t $(THREADS) -R '@RG\tID:$(SRR_ID)\tSM:$(SRR_ID)\tPL:ILLUMINA' $(INDEX_PREFIX) $(FASTQ1) $(FASTQ2) | samtools sort -@ $(THREADS) -o $@ -
	samtools flagstat $@

$(BAM_FILE).bai: $(BAM_FILE)
	samtools index $<

VARIANTS: $(VCF_FILE)

$(VCF_FILE): Makefile $(BAM_FILE) $(BAM_FILE).bai $(REF_GENOME)
	mkdir -p $(@D)
	bcftools mpileup -d 50 --annotate 'INFO/AD,FORMAT/DP,FORMAT/AD,FORMAT/ADF,FORMAT/ADR,FORMAT/SP' \
		-O u -f $(REF_GENOME) $(BAM_FILE) | \
		bcftools call --ploidy 1 --annotate 'FORMAT/GQ' -mv -O u | \
		bcftools norm -f $(REF_GENOME) -d all -O u | \
		bcftools sort --write-index -O z -o $@
	ls -lh $@

batch: GENOME INDEX
	@command -v parallel >/dev/null || { echo "GNU parallel is required for the batch target." >&2; exit 1; }
	@parallel --colsep , --header : --jobs $(JOBS) \
		'$(MAKE) --no-print-directory all SRR_ID={Run} N=$(N) THREADS=$(THREADS)' \
		:::: $(DESIGN)
	$(MAKE) --no-print-directory MERGE_VARIANTS

MERGE_VARIANTS:
	@for vcf in $(VCF_FILES); do \
		test -s "$$vcf" || { echo "Missing per-run VCF: $$vcf (run 'make batch' first)." >&2; exit 1; }; \
	done
	mkdir -p merged_vcf
	bcftools merge --write-index -O z -o merged_vcf/merged-VCF.vcf.gz $(VCF_FILES)


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