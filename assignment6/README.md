# Assignment 6 

## Files:
Load the following file as your reference genome via Genomes -> Load Genome from URL:

    https://data.biostarhandbook.com/courses/2026-appbio/igv/fasta/ebola-1976.fa

Load each sample via File -> Load from URL (leave the index file path empty):

    Sample 1: https://data.biostarhandbook.com/courses/2026-appbio/igv/bam/sample_1.bam
    Sample 2: https://data.biostarhandbook.com/courses/2026-appbio/igv/bam/sample_2.bam
    Sample 3: https://data.biostarhandbook.com/courses/2026-appbio/igv/bam/sample_3.bam
    Sample 4: https://data.biostarhandbook.com/courses/2026-appbio/igv/bam/sample_4.bam
    Sample 5: https://data.biostarhandbook.com/courses/2026-appbio/igv/bam/sample_5.bam


For each sample, provide a paragraph with your best description of the genomic variation relative to the reference genome.


[Info on how to read IGV.](https://help.connected.illumina.com/dragen/dragen-v4.4/product-guide/dragen-v4.4/dragen-dna-pipeline/sv-calling/sv-igv-tutorial)

## Sample 1

Sample 1 has a coverage of approximately 20x with a range of 0x to 37x. At 1,522 there are seven reads with an insert of three bases "GTG". At position 1451 there are 12 bases with an insert of "T". The alignment is fairly clean, but there are a few positions, such as 14,501 where there are disagreements between reads as to what the base call is. Interestingly, in the reference genome, there is a "T" at 736 but on all of the reads of sample 1 there is a "G". However, since there is a lot of agreement between reads, it could be polymorphisms or SNPs. There are a lot of deletions (red) and insertions (dark blue) throughout.

## Sample 2

Sample 2 was a lot less clean when compared to sample 1. Similar to sample 1, the coverage range is between 0 and 37. Despite this, there is a lot more disagreement between reads about base calls. At multiple positions, the reads also disagree with the reference genome. The widespread disagreement between reads concerning base calls makes me think there were widespread sequencing errors or alignment errors. Although it is also possible these are SNPs.

## Sample 3

Similar to sample 2, sample 3 had a lot more disagreement among reads concerning base calls. The coverage of sample 3 ranged between 0x and 167x. Around 1,000 and 6,000 there are 3 duplications which were not as represented on samples one and two. Within this copy number variation, there is a lot of disagreement about the base calls which could either represent sequencing/alignment errors or SNPs. This sample also has a lot of deletions.

## Sample 4

The coverage of sample 4 was between 0x and 78x. The teal (LL) and blue (RR) reads between bases 4,500 and 6,400 indicate a possible inversion. Within this inversion there seem to be a few reads indicating a possible deletion. However, within the possible inversion there is still widespread agreement about the base calls. Throughout the alignment, some reads indicate insertions and deletions. However, at the positions with insertions and deletions, there is not a lot of agreement at the reads at those positions so it may not be correct.

## Sample 5

Similar to sample 4, the coverage is between 0x and 78x. Between bases 4,550 and 5,000 a lot of bases are indicating deletion while between bases 5,000 and 5,450 there are a lot of reads colored neon green to indicate intra-chromosomal translocations. This is then followed by another deletion between bases 5,550 and 6,450. All throughout, there are possible SNPs or more likely sequencing errors since at each position there isn't agreement between reads on the bases. 