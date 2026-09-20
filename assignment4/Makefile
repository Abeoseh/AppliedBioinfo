SHELL := /bin/sh

SRR_ID ?= SRR40309130
N ?= 10

.PHONY: SRR

SRR:
	@echo "Fetching first $(N) spots of $(SRR_ID)"

	## Temporary directory for downloaded files
	mkdir -p maketemp

	fastq-dump \
		-X $(N) \
		--split-files \
		$(SRR_ID) \
		--outdir maketemp

	## Create directory for this SRR accession
	mkdir -p "SRR/$(SRR_ID)/fastq"

	## Move FASTQ files into the SRR-specific directory
	for file in maketemp/*.fastq; do \
		if [ -f "$$file" ]; then \
			mv "$$file" "SRR/$(SRR_ID)/fastq/$$(basename "$$file")"; \
		fi \
	done

	## Run FastQC on the original reads
	echo "Running FastQC on original reads"

	for file in SRR/$(SRR_ID)/fastq/*.fastq; do \
		if [ -f "$$file" ]; then \
			fastqc \
				-o "SRR/$(SRR_ID)/fastq" \
				"$$file"; \
		fi \
	done

	## Directory for trimmed reads
	mkdir -p "SRR/$(SRR_ID)/fastq/trimmed"

	## Check whether paired-end files exist
	if [ -f SRR/$(SRR_ID)/fastq/*_1.fastq ] && \
	   [ -f SRR/$(SRR_ID)/fastq/*_2.fastq ]; then \
		\
		echo "Paired-end reads detected"; \
		\
		for R1 in SRR/$(SRR_ID)/fastq/*_1.fastq; do \
			R2="$${R1%_1.fastq}_2.fastq"; \
			BASE="$$(basename "$${R1%_1.fastq}")"; \
			\
			echo "Running fastp on $$BASE"; \
			\
			fastp \
				-i "$$R1" \
				-I "$$R2" \
				-o "SRR/$(SRR_ID)/fastq/trimmed/$${BASE}_1.trimmed.fastq" \
				-O "SRR/$(SRR_ID)/fastq/trimmed/$${BASE}_2.trimmed.fastq" \
				--detect_adapter_for_pe \
				--cut_front \
				--cut_tail \
				--cut_mean_quality 20 \
				--html "SRR/$(SRR_ID)/fastq/trimmed/$${BASE}.fastp.html" \
				--json "SRR/$(SRR_ID)/fastq/trimmed/$${BASE}.fastp.json"; \
		done \
		\
	else \
		\
		echo "Single-end reads detected"; \
		\
		for R1 in SRR/$(SRR_ID)/fastq/*.fastq; do \
			if [ -f "$$R1" ]; then \
				BASE="$$(basename "$$R1" .fastq)"; \
				\
				echo "Running fastp on $$BASE"; \
				\
				fastp \
					-i "$$R1" \
					-o "SRR/$(SRR_ID)/fastq/trimmed/$${BASE}.trimmed.fastq" \
					--cut_front \
					--cut_tail \
					--cut_mean_quality 20 \
					--html "SRR/$(SRR_ID)/fastq/trimmed/$${BASE}.fastp.html" \
					--json "SRR/$(SRR_ID)/fastq/trimmed/$${BASE}.fastp.json"; \
			fi \
		done \
	fi

	## Run FastQC on trimmed reads
	echo "Running FastQC on trimmed reads"

	for file in SRR/$(SRR_ID)/fastq/trimmed/*.fastq; do \
		if [ -f "$$file" ]; then \
			fastqc \
				-o "SRR/$(SRR_ID)/fastq/trimmed" \
				"$$file"; \
		fi \
	done

	## Remove temporary files
	rm -rf maketemp

	@echo "Pipeline complete."
