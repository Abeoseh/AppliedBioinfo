ASSEMBLY := GCF_977971745.1_Znev_1.0

URL := https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/977/971/745/$(ASSEMBLY)

DATA := data

GZ_FILES := \
	$(DATA)/$(ASSEMBLY)_genomic.fna.gz \
	$(DATA)/$(ASSEMBLY)_genomic.gff.gz

FILES := \
	$(DATA)/$(ASSEMBLY)_genomic.fna \
	$(DATA)/$(ASSEMBLY)_genomic.gff

.PHONY: all clean

all: $(FILES)

$(DATA):
	mkdir -p $(DATA)

$(DATA)/%.fna.gz: | $(DATA)
	curl -L -o $@ $(URL)/$(notdir $@)

$(DATA)/%.gff.gz: | $(DATA)
	curl -L -o $@ $(URL)/$(notdir $@)

$(DATA)/%.fna: $(DATA)/%.fna.gz
	gunzip -k $<

$(DATA)/%.gff: $(DATA)/%.gff.gz
	gunzip -k $<

clean:
	rm -rf $(DATA)