### Answers

Prerequisites

    Select a genome and an annotation file.
        The genome I chose is Zootermopsis nevadensis (termites)
    Load both into a genome visualization platform.
        I chose IGV

Note: the data files are not available since they were too large to host on github:
> remote: error: File week02/data/GCF_977971745.1_Znev_1.0_genomic.fna is 556.50 MB; this exceeds GitHub's file size limit of 100.00 MB

> remote: error: File week02/data/GCF_977971745.1_Znev_1.0_genomic.gff is 292.36 MB; this exceeds GitHub's file size limit of 100.00 MB

- **Makefile Usage**
    - the command to use the make file is `make` which will download and unzip the genome (fna) and annotatio (gff) files

- **How large is the genome? How many chromosomes does it have?**
![assembled_chromosomes info](images/assembled_chromosomes.png)
[info](https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_977971745.1/)
    - The contigs/sequences were not assembled to the chromosome level according to NCBI. However, using `seqkits` I could still get some stats out:

    ```
    $ seqkit stats data/GCF_977971745.1_Znev_1.0_genomic.fna
    ```
    Output:
    ```
    file                                       format  type  num_seqs      sum_len  min_len      avg_len     max_len
    data/GCF_977971745.1_Znev_1.0_genomic.fna  FASTA   DNA        322  576,279,275   14,514  1,789,687.2  27,517,609

    ```
    This genome is 576,279,275 base pairs long with an unknown number of chromosomes.


- **Number of Annotations**
    - From within the `week02` folder I ran
    ```
    awk '!/^#/ {count[$3]++} END {
    for (type in count) {
        print type, count[type]
        total += count[type]
    }
    print "total", total
    }' data/GCF_977971745.1_Znev_1.0_genomic.gff
    ```
    output:
    
    |feature|count|
    --------|------
    |scaRNA |1|
    |SRP_RNA |17|
    |sequence_feature |1|
    |mRNA| 40417|
    |lncRNA |4302|
    |rRNA |363|
    |exon| 502098|
    |region| 322|
    |CDS| 408933|
    |RNase_P_RNA| 1|
    |gene| 17244|
    |cDNA_match| 339|
    |pseudogene| 541|
    |transcript| 3019|
    |RNase_MRP_RNA| 1|
    |snoRNA| 21|
    |tRNA| 233|
    |snRNA| 90|
    |total| 977943|

- **How complete is this genomic build in your opinion?**
    - I think this genome is fairly complete. There should be chromosomes which were not present. The number of bases (576 Mb) roughly align with the [esimated genome size of 562 Mb](https://metazoa.ensembl.org/Zootermopsis_nevadensis/Info/Annotation/) which indicates a correct sequencing of the genome.

- **How tightly packed are the genes in this genome? Estimate the gene-to-gene distance via the browser.**
    - Using the IGV browser, I can estimate that the distance is approximately 108 using a few genes. However, when I write a script to confirm, I get an average gene-to-gene distance of average distance: 11,669 and a median distance of 1155. This is because the smallest distance is 0 (which means the genes are overlapping) and the largest distance is 2,177,515.

equations: $\sum \frac{start\:position\:of\:next\:gene - end\:position\:of\:previous\:gene - 1}{n\_positions} = average\:position$



- **Pick a coordinate on the chromosome and visually inspect the sequence regions around it.**
    - The contigs were not assembled to chromosome level. But on contig NW_028259133.1 there is gene LOC147875140 with GeneID 147875140 it spans positions 52541 from 62862. It is a peroxisomal multifunctional enzyme type 2-like. Directly preceeding the gene there is a A C rich area for approximately 16 bases. After the gene is enriched in G, A, T but not C.




- **Describe all six reading frames (codons) that the coordinate could be part of.**
    - Since the start codon starts at AUG where U would correspond to the T. The gene is on the negative strand. On the forward strand, the first open reading frame has a lot of false starts, there is a 3 amino acid protein from 52,594 to 52,598 many other possible ORF throughout. There are also multiple potential proteins on ORF 2 and ORF 3 though most correspond with small amino acid chains. The protein is on the reverse strand starting at 52,744 and ending at 52,578 (on the forward strand). The first open reading frame carries the protein and similar to the forward strand, all three ORF have a lot of false starts for proteins. 


- **Identify the type of feature displayed as a data track. Color features by their strand orientation.**

The feature in image 1 on the data track is gene LOC147875139. It is on the forward track which is identifiable my the blue track. The feature in image 2 on the data track is gene LOC147875140 which is identifiably on the reverse track since the track is pink.

![alt text](images/forward_gene_LOC147875139.png)
**forward gene on the data track**


![alt text](images/reverse_gene_LOC147875140.png)
**reverse gene on the data track**

