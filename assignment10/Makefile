
SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c
.DELETE_ON_ERROR:
.ONESHELL:

# ============================================================
# Reference genome and annotation
# Saccharomyces cerevisiae
# ============================================================

GENOME_URL ?= https://ftp.ensemblgenomes.ebi.ac.uk/pub/fungi/release-62/fasta/saccharomyces_cerevisiae/dna/Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa.gz

ANNOTATION_URL ?= https://ftp.ensemblgenomes.ebi.ac.uk/pub/fungi/release-62/gff3/saccharomyces_cerevisiae/Saccharomyces_cerevisiae.R64-1-1.62.gff3.gz

REF_FILE ?= Saccharomyces_cerevisiae.R64-1-1.dna.toplevel.fa
ANN_FILE ?= Saccharomyces_cerevisiae.R64-1-1.62.gff3

REF_GENOME := ref_genome/$(REF_FILE)
REF_ANNOTATION := ref_genome/$(ANN_FILE)
INDEX_PREFIX := ref_genome/index/sacCer3

# ============================================================
# Per-run parameters
# ============================================================

SRR_ID ?= SRR25220267
N ?= 140000
THREADS ?= 2
JOBS ?= 2
DESIGN ?= design.csv

FASTQ_DIR := $(SRR_ID)/fastq
FASTQ1 := $(FASTQ_DIR)/$(SRR_ID)_1.fastq
FASTQ2 := $(FASTQ_DIR)/$(SRR_ID)_2.fastq
FASTQ_STAMP := $(FASTQ_DIR)/.spots-$(N).complete

BAM_FILE := $(SRR_ID)/bam/$(SRR_ID).bam

# ============================================================
# MACS3 parameters
# ============================================================

MACS3 ?= macs3

# Effective genome size for S. cerevisiae
EFFECTIVE_GENOME_SIZE ?= 1.2e7

MACS_QVALUE ?= 0.01

PEAK_DIR := peaks

# ============================================================
# IGV parameters
# ============================================================

IGV_MANIFEST := peaks/igv_manifest.tsv
IGV_SESSION := peaks/igv_session.xml
IGV_CMD ?= igv

# ============================================================
# Dynamic sample and case/control discovery
# ============================================================

DESIGN ?= design.csv

RUNS := $(shell python3 design.py runs $(DESIGN))

PEAK_PAIRS := $(shell python3 design.py pairs $(DESIGN))

ifeq ($(strip $(RUNS)),)
$(error No samples found in $(DESIGN))
endif

ifeq ($(strip $(PEAK_PAIRS)),)
$(error No matched case/control pairs found in $(DESIGN))
endif

# ============================================================
# Main targets
# ============================================================

.PHONY: all GENOME FASTQs INDEX ALIGN batch PEAKS IGV clean

all: GENOME ALIGN

GENOME: $(REF_GENOME) $(REF_ANNOTATION)

# ============================================================
# Download reference genome
# ============================================================

$(REF_GENOME):
	mkdir -p $(@D)
	curl -fsSL $(GENOME_URL) | gzip -dc > $@.tmp
	mv $@.tmp $@

$(REF_ANNOTATION):
	mkdir -p $(@D)
	curl -fsSL $(ANNOTATION_URL) | gzip -dc > $@.tmp
	mv $@.tmp $@

# ============================================================
# Download FASTQ files
# ============================================================

FASTQs: $(FASTQ_STAMP)

$(FASTQ_STAMP):
	mkdir -p $(FASTQ_DIR)
	if [[ -s $(FASTQ1) && -s $(FASTQ2) && \
	    $$(( $$(wc -l < $(FASTQ1)) / 4 )) -eq $(N) && \
	    $$(( $$(wc -l < $(FASTQ2)) / 4 )) -eq $(N) ]]; then \
	    touch $@; \
	else \
	    rm -f $(FASTQ1) $(FASTQ2); \
	    fastq-dump -X $(N) --split-files $(SRR_ID) --outdir $(FASTQ_DIR); \
	    test -s $(FASTQ1) && test -s $(FASTQ2); \
	    touch $@; \
	fi
	seqkit stats $(FASTQ1) $(FASTQ2)

# ============================================================
# BWA index
# ============================================================

INDEX: $(INDEX_PREFIX).bwt

$(INDEX_PREFIX).bwt: $(REF_GENOME)
	mkdir -p $(@D)
	bwa index -a is -p $(INDEX_PREFIX) $(REF_GENOME)

# ============================================================
# Alignment
# ============================================================

ALIGN: $(BAM_FILE) $(BAM_FILE).bai

$(BAM_FILE): Makefile $(FASTQ_STAMP) $(INDEX_PREFIX).bwt
	mkdir -p $(@D)
	bwa mem -t $(THREADS) \
	    -R '@RG\tID:$(SRR_ID)\tSM:$(SRR_ID)\tPL:ILLUMINA' \
	    $(INDEX_PREFIX) $(FASTQ1) $(FASTQ2) | \
	    samtools sort -@ $(THREADS) -o $@ -
	samtools flagstat $@

$(BAM_FILE).bai: $(BAM_FILE)
	samtools index $<

# ============================================================
# Batch alignment
# ============================================================

batch: GENOME INDEX design.py $(DESIGN)
	@command -v parallel >/dev/null || { \
	    echo "GNU parallel is required." >&2; \
	    exit 1; \
	}
	@parallel --jobs $(JOBS) \
	    '$(MAKE) --no-print-directory all SRR_ID={} N=$(N) THREADS=$(THREADS)' \
	    ::: $(RUNS)

# ============================================================
# MACS3 case/control peak calling
# ============================================================

PEAKS: batch
	mkdir -p $(PEAK_DIR)
	@set -euo pipefail; \
	for pair in $(PEAK_PAIRS); do \
	    CASE=$${pair%%:*}; \
	    CONTROL=$${pair##*:}; \
	    TF=$$(python3 -c 'import csv,sys; r=next(x for x in csv.DictReader(open(sys.argv[1])) if x["Run"]==sys.argv[2]); print(r["TranscriptionFactor"])' $(DESIGN) $$CASE); \
	    OUTDIR=$(PEAK_DIR)/$$TF; \
	    mkdir -p $$OUTDIR; \
	    echo "Calling peaks: $$CASE vs $$CONTROL ($$TF)"; \
	    $(MACS3) callpeak \
	        -t $$CASE/bam/$$CASE.bam \
	        -c $$CONTROL/bam/$$CONTROL.bam \
	        -f BAMPE \
	        -n $$CASE \
	        -g $(EFFECTIVE_GENOME_SIZE) \
	        -q $(MACS_QVALUE) \
	        --outdir $$OUTDIR; \
	done


# ============================================================
# IGV session generation and launch
# ============================================================


# ============================================================
# IGV session generation and launch
# ============================================================


# ============================================================
# IGV session generation and launch
# ============================================================

IGV: PEAKS
	@set -euo pipefail
	@mkdir -p $(PEAK_DIR)
	@printf 'Case\tControl\tPeak\tCase_BAM\tControl_BAM\n' > $(IGV_MANIFEST)
	@for pair in $(PEAK_PAIRS); do \
	    CASE=$${pair%%:*}; \
	    CONTROL=$${pair##*:}; \
	    find $(PEAK_DIR) -type f \
	        -name "$${CASE}_peaks.narrowPeak" | \
	    while IFS= read -r PEAK; do \
	        printf '%s\t%s\t%s\t%s\t%s\n' \
	            "$$CASE" \
	            "$$CONTROL" \
	            "$$PEAK" \
	            "$$CASE/bam/$$CASE.bam" \
	            "$$CONTROL/bam/$$CONTROL.bam" \
	            >> $(IGV_MANIFEST); \
	    done; \
	done
	@test "$$(wc -l < $(IGV_MANIFEST))" -gt 1 || { \
	    echo "No MACS3 peak files found!" >&2; exit 1; \
	}
	@REF_GENOME="$(REF_GENOME)" \
	IGV_MANIFEST="$(IGV_MANIFEST)" \
	IGV_SESSION="$(IGV_SESSION)" \
	python3 igv_session.py
	@echo "IGV session created: $(IGV_SESSION)"
	@if command -v $(IGV_CMD) &>/dev/null; then \
	    echo "Launching IGV..."; \
	    $(IGV_CMD) "$(IGV_SESSION)"; \
	else \
	    echo "IGV not found. To open the session manually:"; \
	    echo "  1. Open IGV from your Applications or Downloads folder"; \
	    echo "  2. Go to File → Open Session"; \
	    echo "  3. Navigate to: $(IGV_SESSION)"; \
	fi


# ============================================================
# Clean
# ============================================================

clean:
	rm -rf $(PEAK_DIR)
