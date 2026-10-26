# Assignment 8

## Determining coverage (10x)
$coverage = \frac{read\\_length * num\\_reads}{genome\\_size}$


- ERR15846824 ("Bacillus subtilis subsp. subtilis str. 168")
Sequenced on Illumina MiSeq which tends to generate reads of length 300 bases (or 600 bases for paired end reads)

- DRR1105562 ("Bacillus subtilis subsp. subtilis str. 168")
Sequenced on Illumina HiSeq 2500 which tends to generate reads of length 300 bases (or 600 bases for paired end reads)

- ERR15846822 ("Bacillus subtilis subsp. subtilis str. 168")
Sequenced on Illumina MiSeq which tends to generate reads of length 300 bases (or 600 bases for paired end reads)


For all three samples I will use the formula: </br>
$$
num\_reads = \frac{genome\\_size * coverage}{read\\_length}
= \frac{3,918,596*10x}{600} = 65,309.9333
$$
For paired ends I will do do $65,309.9333/2=32654.9667$ or $32655$ since I am using paired end reads.</br></br>
Since I am doing paired end reads, each spot corresponds to 2 reads so I will use `fastq-dump -X 32655` or in my make file `-N 32655`

## Make file

### parameters:
-   GENOME_URL - the URL of the reference genome
    - default: https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/015/785/GCF_000015785.2_ASM1578v2/GCF_000015785.2_ASM1578v2_genomic.fna.gz

- SRR_ID - the SRR id of the sample
    - default: ERR15846824

- N - number of spots for fastq dump
    - default: 32655

- REF_FILE - file name of the reference genome
    - default: GCF_000015785.2_ASM1578v2_genomic.fna

- MERGE - merge all the found vcf files
    - default: 0 (to merge the vcf files use MERGE=1)

```bash
make SRR_ID=ERR15846824
make SRR_ID=DRR1105562
make SRR_ID=ERR15846822 MERGE=1
```


## Visualizing the variants
There were no variants in **ERR15846824** and **ERR15846822**


**DRR1105562**

![alt text](images/vcf_stats_DRR1105562.png)


ERR15846822 and ERR15846824 have no variant positions. They are both part of the same study and bioproject (PRJEB102831) which may explain this lack of variation. Interestingly, DRR1105562 has variants all throught the sample.


## IGV
![alt text](images/igv_with_translation.png)


From this we can see that the three "Bacillus subtilis subsp. subtilis str. 168" species have a high level of agreement as to what the variants are. Although DRR1105562 has high levels of overlap with ERR15846822 and ERR15846824, there is some distinction which could be due to technical variation in sequencing due to being processed in a different labratory. 

## Variant Example

I used BCFTools to annotate alleles. There are a lot of gyr genes which are mutated, all on the forward strand. Most of the mutations are on the reverse strand (457/875) and most were missensene mutations (552/875).

| POS   | REF | ALT | Consequence | Gene | Transcript | Biotype        | Strand | Amino acid change | DNA change |
|-------|-----|-----|-------------|------|------------|----------------|--------|------------------|------------|
| 5414  | A   | T   | missense    | gyrB | CAB11782   | protein_coding | +      | 183E>183V        | 5414A>T    |
| 7687  | A   | G   | missense    | gyrA | CAB11783   | protein_coding | +      | 232K>232E        | 7687A>G    |
| 8942  | T   | A   | missense    | gyrA | CAB11783   | protein_coding | +      | 650M>650K        | 8942T>A    |
| 8950  | C   | T   | missense    | gyrA | CAB11783   | protein_coding | +      | 653R>653C        | 8950C>T    |
| 20205 | G   | A   | missense    | pdxT | CAB11788   | protein_coding | +      | 80A>80T          | 20205G>A   |
| 24411 | A   | T   | synonymous  | sleL | CAB11792   | protein_coding | -      | 247P             | 24411A>T   |
| 24851 | A   | G   | missense    | sleL | CAB11792   | protein_coding | -      | 101S>101P        | 24851A>G   |
| 25444 | A   | T   | missense    | yaaI | CAB11793   | protein_coding | -      | 108L>108H        | 25444A>T   |
| 28541 | A   | G   | missense    | ebfC | CAB11796   | protein_coding | +      | 5M>5V            | 28541A>G   |
| 37539 | A   | G   | missense    | yaaN | CAB11802   | protein_coding | +      | 354I>354M        | 37539A>G   |
| 44853 | T   | C   | missense    | abrB | CAB11813   | protein_coding | -      | 96K>96E          | 44853T>C   |
