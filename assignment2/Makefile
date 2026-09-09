ASSEMBLY := GCF_977971745.1_Znev_1.0

URL := https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/977/971/745/$(ASSEMBLY)

FILES := \
	$(ASSEMBLY)_genomic.fna.gz \
	$(ASSEMBLY)_genomic.gff.gz

.PHONY: all clean

all: $(FILES)

%.gz:
	curl -L -O $(URL)/$@

clean:
	rm -f $(FILES)