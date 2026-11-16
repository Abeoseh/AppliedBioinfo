transcript_matrix <- "results/transcript_counts.csv"
if (!file.exists(transcript_matrix)) {
  stop("Missing ", transcript_matrix, "; run src/combine_transcript_counts.r first.")
}
transcript_counts <- read.csv(
  transcript_matrix,
  stringsAsFactors = FALSE,
  check.names = FALSE
)
sample_columns <- names(transcript_counts)[-(1:3)]

gene_name_counts <- vapply(
  split(transcript_counts$gene_name, transcript_counts$gene_id),
  function(names) length(unique(names)),
  integer(1)
)
if (any(gene_name_counts > 1)) {
  stop("At least one gene ID maps to multiple gene names in the transcript matrix.")
}
gene_metadata <- transcript_counts[
  !duplicated(transcript_counts$gene_id),
  c("gene_id", "gene_name")
]
gene_metadata <- gene_metadata[order(gene_metadata$gene_id), ]
gene_counts <- rowsum(
  as.matrix(transcript_counts[sample_columns]),
  group = transcript_counts$gene_id,
  reorder = FALSE
)
gene_counts <- gene_counts[gene_metadata$gene_id, , drop = FALSE]

result <- data.frame(
  gene = gene_metadata$gene_id,
  gene_name = gene_metadata$gene_name,
  gene_counts,
  check.names = FALSE,
  stringsAsFactors = FALSE
)
write.csv(result, "results/gene_counts.csv", row.names = FALSE)
message("Wrote ", nrow(result), " genes across ", ncol(gene_counts),
        " samples to results/gene_counts.csv")
