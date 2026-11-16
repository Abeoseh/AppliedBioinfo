# Assignment 12: Salmon count matrices

This assignment combines transcript-level Salmon quantifications into two raw-count matrices: one row per transcript and one row per gene. The gene-level counts are the sums of the transcript counts assigned to each gene. Both matrices include gene IDs and gene names.

## Files and inputs

- `gene_level_count_matrix/design.csv` lists the six samples (`HBR_1`-`HBR_3` and `UHR_1`-`UHR_3`) and their groups.
- `gene_level_count_matrix/counts/<sample>/quant.sf` contains each Salmon quantification.
- `gene_level_count_matrix/gtf/chr22.gtf` maps transcript IDs to gene IDs and gene names.
- `src/combine_transcript_counts.r` builds the transcript matrix from the Salmon `NumReads` column and the GTF mapping.
- `src/combine_gene_counts.r` sums transcript counts by gene ID.
- The output files are `results/transcript_counts.csv` and `results/gene_counts.csv`.

The existing Salmon quantifications in `gene_level_count_matrix/` can be reused. To recreate them from the tutorial data instead, use `make data` followed by `make quantify`. The quantification step requires Salmon and GNU Parallel.

## Run

From this assignment directory, in WSL with the course environment activated:

```bash
conda activate bioinfo
```

The assignment also asks you to view the coverage tracks and GTF in IGV. The `gene_level_count_process/Makefile` builds the genome-based alignments, coverage tracks, and featureCounts files. If these outputs are not already present, run:

```bash
make -C gene_level_count_process data
make -C gene_level_count_process batch
```

With IGV open and its port 60151 enabled, load the GTF and all coverage tracks using:

```bash
make -C gene_level_count_process igv
```

The `gene_level_count_matrix/Makefile` performs transcript-level Salmon quantification. The top-level `make matrices` target invokes it (including its data and batch targets), then runs both R scripts:

```bash
make matrices
```

If Salmon quantifications are already present, the nested Makefile can reuse them. To run only the matrix scripts after quantification:

```bash
Rscript src/combine_transcript_counts.r
Rscript src/combine_gene_counts.r
```

For a complete run from a fresh checkout, activate `bioinfo`, run the two `gene_level_count_process` commands above and view the tracks in IGV, then run `make matrices`. The scripts use base R; no additional R packages are required. The sample columns follow the order in `gene_level_count_matrix/design.csv`. Run commands from this assignment directory because the scripts use paths relative to it.

## Checking the results

The transcript matrix uses Salmon's estimated `NumReads` (raw estimated counts), not TPM. It has transcript ID, gene ID, gene name, then one count column per sample. The gene matrix has gene ID, gene name, then the same sample columns; each sample's gene count is the sum of its transcript counts for that gene. The scripts stop with an error if required inputs are missing, Salmon files have unexpected columns or duplicate transcript IDs, or a quantified transcript has no GTF mapping.

After running, inspect the headers and compare selected rows across files. For a gene, its value in each column of `gene_counts.csv` should equal the sum of the corresponding transcript rows for that gene in `transcript_counts.csv`. This check also ensures counts, rather than TPM, were summarized.

## Does the count matrix support what was seen in IGV last week?

Yes, for the genes highlighted in assignment 11. The [IGV screenshot of XBP1](../assignment11/images/strong_expressed.png) showed coverage in all six samples, with visibly higher signal in the UHR tracks than in the HBR tracks. In this transcript-summed gene matrix, XBP1 has counts of 65, 94, and 75 in HBR and 1,060, 632, and 743 in UHR. Each UHR replicate is higher than every HBR replicate; the group means are about 78 and 812, respectively. The earlier genome-based featureCounts matrix shows the same pattern for XBP1 (65, 95, 77 in HBR; 1,078, 637, 762 in UHR).

The assignment 11 IGV notes also identified EP300-AS1 as not expressed. Its count is zero in all six samples in both the transcript-summed matrix and the earlier featureCounts files, which is consistent with that observation. Together, these examples support the qualitative IGV observations, including the stronger UHR XBP1 signal and the lack of detected EP300-AS1 expression. Raw counts and coverage are not directly interchangeable, and these comparisons alone do not establish statistical differential expression; sample sequencing depth and normalization must be considered for that.

### Where the two methods disagree

The two count-generation methods being compared here are Salmon transcript-level quantification followed by gene summation, and assignment 11's genome-alignment featureCounts. They are not numerically interchangeable. Of the 1,369 shared genes, 743 have at least one sample with different counts; for 281 genes, one method reports zero where the other reports a nonzero count in at least one sample. Salmon's estimated `NumReads` can be fractional, unlike featureCounts' integer counts, so exact equality is not expected.

Some differences are larger. For example, Salmon gives MIF counts of 113-147 in HBR and about 349-530 in UHR, while featureCounts gives 14-22 and 39-63, respectively. Both methods show higher UHR MIF counts, but the count scale differs substantially. For POLR2F, Salmon's group means are about 54 in HBR and 81 in UHR, whereas featureCounts' means are about 20 and 9, reversing the apparent group direction. These discrepancies mean the agreement on XBP1 and EP300-AS1 is qualitative and gene-specific, not proof that the methods agree for every gene. The methods quantify reads differently, and these are unnormalized counts, so the discrepancies should be investigated and counts normalized before drawing broader or statistical conclusions.

## AI prompting and challenges

Usually, I do a mix of AI prompting and using ChatGPT. The base `Makefile` used in most of the assignments was writen by myself and edited using ChatGPT. However, in this assignment I heavily relied on ChatGPT. 


By mostly using ChatGPT I learned that useful AI prompting should name the input files, the Salmon output format, the required output paths, and whether the matrix needs raw counts or normalized expression. 


A main challenge is understanding what was done. The AI agent generates a lot of code in one sitting so it is very hard to understand what it did. Due to this, it's also hard to know if what is did is correct.