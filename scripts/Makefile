
# Make sure we run in bash.
SHELL = bash

# Accession number for reference genome.
ACC ?= AF086833

# Accession number for the SRA run.
SRR ?= SRR1553425

# Number of compute cores.
CPU ?= 4

# Number of test reads used when running testdata.
LIMIT ?=10000

# GenBank reference file.
GBK=${ACC}.gbk

# Fasta reference file.
REF=refs/${ACC}.fa

# GFF reference file.
GFF=refs/${ACC}.gff

# Temporary directory used only with fasterq-dump.
# See also: https://www.moritzs.de/linux/thank_you_sra/
TMP=tmp

# All names will have this common element.
ROOT=${SRR}-${ACC}

# Alignment file.
BAM=bam/${ROOT}.bam

# Variant file.
VCF=vcf/${ROOT}.vcf.gz

# The annotated VCF file.
ANN=vcf/${ROOT}.annotated.vcf.gz

# The SNPeff database.
SNPEFF = data/${ACC}/snpEffectPredictor.bin

# Original read names.
R1=reads/${SRR}_1.fastq
R2=reads/${SRR}_2.fastq

# Name of the quality trimmed read pairs.
Q1=reads/${SRR}_1P.fq
Q2=reads/${SRR}_2P.fq

# The BWA index.
IDX=${REF}.amb

# Phony targets instruct make to use these as rules only.
.PHONY: data vcf

# Check that required executables exist.
EXE = bio bwa samtools bcftools snpEff trimmomatic
K := $(foreach exec,$(EXE),\
        $(if $(shell which $(exec)),ok,$(error "Program: $(exec) not found.")))

# Print usage.
all:
	@echo "USAGE:"
	@echo
	@echo "  make vcf         # generates a VCF file"
	@echo
	@echo "  make clean       # removes test data"
	@echo "  make realclean   # removes all intermediate files"
	@echo "  make data        # downloads the full dataset"
	@echo ""
	@echo "DEFAULTS:"
	@echo ""
	@echo "   ACC=${ACC}  SRR=${SRR}  CPU=${CPU}  LIMIT=${LIMIT}"
	@echo ""

# Generate the annotated VCF
vcf: ${ANN}

# Removes all files created by operations in this file.
clean:
	rm -rf reads/${SRR}* ${TMP}

# Removes all files created by operations in this file.
realclean:
	rm -rf refs reads ${TMP} vcf bam data tmp snpEff.config

# Rule to make the GFF file.
${GFF}:
	mkdir -p refs
	bio fetch ${ACC} -format gff > ${GFF}

# Rule to make the reference genome.
# We stick the GFF here as a dependency so that it gets downloaded early on.
${REF}: ${GFF}
	mkdir -p refs
	bio fetch ${ACC} -format fasta > ${REF}
	samtools faidx ${REF}

# The index depends on the reference genome.
${IDX}: ${REF}
	bwa index ${REF}
	echo ${IDX}

# Download a subset (test) of the SRA data.
${R1} ${R2}:
	mkdir -p reads
	fastq-dump -F -X ${LIMIT} --split-files -O reads ${SRR}

# Download the full SRA run
data:
	mkdir -p reads ${TMP}
	fasterq-dump -e ${CPU} -t ${TMP} -f -x -p  -O reads --split-files ${SRR}

# Apply quality control to the reads.
${Q1} ${Q2}: ${R1} ${R2}

	# Will generate both adapters.
	echo ">illumina" > reads/adapter.fa
	echo "AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC" >> reads/adapter.fa
	echo ">nextera" >> reads/adapter.fa
	echo "CTGTCTCTTATACACATCTCCGAGCCCACGAGAC" >> reads/adapter.fa

	# Apply the trimming.
	trimmomatic PE -threads ${CPU} -phred33 -basein reads/${SRR}_1.fastq -baseout reads/${SRR}.fq\
		ILLUMINACLIP:reads/adapter.fa:2:30:5 SLIDINGWINDOW:4:15 MINLEN:50

# BAM file depends on the BWA index and reads.
${BAM}: ${IDX} ${Q1} ${Q2}
	mkdir -p bam
	# Note how we filter alignment for mapped reads only.
	bwa mem -t ${CPU} ${REF} ${Q1} ${Q2} | samtools view -b -F 4 | samtools sort -@ ${CPU} > ${BAM}
	samtools index ${BAM}
	samtools flagstat ${BAM}

# The VCF file depends on the BAM file.
${VCF}: ${BAM}
	mkdir -p vcf
	bcftools mpileup -O v -f ${REF} ${BAM}  | bcftools call --ploidy 1 -mv -O z -o ${VCF}
	bcftools index ${VCF}
	@echo -e "\n# VCF file: ${VCF}\n"

# Building a custom snpEff database.
${SNPEFF}:
	# Snpeff needs the files in specific folders.
	mkdir -p data/${ACC}

	# Download the GenBank file, has to be called genes.gbk.
	bio fetch ${ACC} > data/${ACC}/genes.gbk

	# Append entry to current genome to the config.
	echo "${ACC}.genome : ${ACC}" >> snpEff.config

	# Build the snpEff database.
	snpEff build -v ${ACC}

# Uses snpEff to annotate the variants.
${ANN}: ${VCF} ${SNPEFF}
	snpEff -v ${ACC} ${VCF} | bcftools view -O z > ${ANN}
	bcftools index ${ANN}
	@mv snpEff_*.*  vcf/
	@echo  -e "\n# Annotated VCF file: ${ANN}\n"


