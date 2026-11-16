design_file <- "gene_level_count_matrix/design.csv"
counts_dir <- "gene_level_count_matrix/counts"
gtf_file <- "gene_level_count_matrix/gtf/chr22.gtf"
output_file <- "results/transcript_counts.csv"

required_files <- c(design_file, gtf_file)
missing_files <- required_files[!file.exists(required_files)]
if (length(missing_files) > 0) {
  stop("Missing required file(s): ", paste(missing_files, collapse = ", "))
}

design <- read.csv(design_file, stringsAsFactors = FALSE, check.names = FALSE)
if (!all(c("sample", "group") %in% names(design)) || nrow(design) == 0) {
  stop("design.csv must contain sample and group columns and at least one sample.")
}
if (anyDuplicated(design$sample)) {
  stop("design.csv contains duplicate sample names.")
}

quant_files <- file.path(counts_dir, design$sample, "quant.sf")
missing_quant <- quant_files[!file.exists(quant_files)]
if (length(missing_quant) > 0) {
  stop("Missing Salmon quantification file(s): ", paste(missing_quant, collapse = ", "))
}

gtf <- read.delim(
  gtf_file, header = FALSE, sep = "\t", quote = "",
  comment.char = "#", stringsAsFactors = FALSE
)
transcript_rows <- gtf[gtf[[3]] == "transcript", 9, drop = FALSE]
attributes <- transcript_rows[[1]]
extract_attribute <- function(attribute, field) {
  matches <- regexec(paste0('(?:^|;\\s*)', field, ' "([^"]+)"'), attribute, perl = TRUE)
  values <- regmatches(attribute, matches)
  vapply(values, function(x) if (length(x) >= 2) x[2] else NA_character_, character(1))
}
tx2gene <- data.frame(
  transcript = extract_attribute(attributes, "transcript_id"),
  gene_id = extract_attribute(attributes, "gene_id"),
  gene_name = extract_attribute(attributes, "gene_name"),
  stringsAsFactors = FALSE
)
tx2gene <- unique(tx2gene[!is.na(tx2gene$transcript) & !is.na(tx2gene$gene_id), ])
if (anyDuplicated(tx2gene$transcript)) {
  stop("GTF maps at least one transcript to multiple gene IDs.")
}

quantifications <- lapply(quant_files, function(path) {
  read.delim(path, stringsAsFactors = FALSE, check.names = FALSE)
})
names(quantifications) <- design$sample
for (i in seq_along(quantifications)) {
  quant <- quantifications[[i]]
  if (!all(c("Name", "NumReads") %in% names(quant))) {
    stop("Salmon file is missing Name or NumReads: ", quant_files[i])
  }
  if (anyDuplicated(quant$Name)) {
    stop("Duplicate transcript IDs in Salmon file: ", quant_files[i])
  }
}

transcript_ids <- unique(unlist(lapply(quantifications, `[[`, "Name")))
counts <- matrix(
  0, nrow = length(transcript_ids), ncol = length(quantifications),
  dimnames = list(transcript_ids, design$sample)
)
for (sample in design$sample) {
  quant <- quantifications[[sample]]
  counts[quant$Name, sample] <- quant$NumReads
}

mapping_index <- match(transcript_ids, tx2gene$transcript)
if (anyNA(mapping_index)) {
  stop(
    "GTF does not provide transcript/gene annotations for ",
    sum(is.na(mapping_index)), " transcript(s); refusing to omit mappings."
  )
}
gene_ids <- tx2gene$gene_id[mapping_index]
gene_names <- tx2gene$gene_name[mapping_index]
gene_names[is.na(gene_names) | gene_names == ""] <- gene_ids[
  is.na(gene_names) | gene_names == ""
]

result <- data.frame(
  transcript = transcript_ids,
  gene_id = gene_ids,
  gene_name = gene_names,
  counts,
  check.names = FALSE,
  stringsAsFactors = FALSE
)
dir.create("results", showWarnings = FALSE)
write.csv(result, output_file, row.names = FALSE)
message("Wrote ", nrow(result), " transcripts across ", ncol(counts),
        " samples to ", output_file)
