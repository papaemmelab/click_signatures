# Single Sample SNP mutation signature analysis using MutationalPatterns
options(warn=1)
library(argparse)

parser = ArgumentParser(description="SNP mutation signature analysis using MutationalPatterns")
parser$add_argument("--outdir", required=TRUE, help="Output Directory")
parser$add_argument("--id", type="character", required=TRUE, help="ID of Sample")
parser$add_argument("--vcf", required=TRUE, help="SNP VCF File")
parser$add_argument("--sigprob", required=TRUE, help="Signature Probrability File")

args = parser$parse_args()

# Go to outdir
setwd(args$outdir)

suppressMessages(library("VariantAnnotation"))

vcf_file = args$vcf
sample_name = args$id
ref_genome = "BSgenome.Hsapiens.UCSC.hg19"

suppressMessages(library(ref_genome, character.only = TRUE))
suppressMessages(library(MutationalPatterns))
suppressMessages(library(RColorBrewer))

# Read in VCF
vcfs = read_vcfs_as_granges(vcf_file, sample_name, ref_genome)

# Get type of mutations and context
type_occurrences = mut_type_occurrences(vcfs, ref_genome)
mutation_matrix = mut_matrix(vcf_list=vcfs, ref_genome=ref_genome)

typeoc = t(type_occurrences)
typeoc = data.frame(rownames(typeoc), typeoc)
colnames(typeoc) = c("Type", sample_name)
write.table(typeoc, "type_occurrences.tsv", sep="\t", quote=FALSE, row.names=FALSE)

png(filename="type_occurrences.png", type="cairo", width = 8, height = 6, units = 'in', res=600)
suppressWarnings(plot_spectrum(type_occurrences, CT = TRUE, legend = TRUE))
graphics.off()

mutmat = data.frame(rownames(mutation_matrix), mutation_matrix)
colnames(mutmat) = c("Context", sample_name)
write.table(mutmat, "context.tsv", sep="\t", quote=FALSE, row.names=FALSE)

# sp_url <- paste("http://cancer.sanger.ac.uk/cancergenome/assets/","signatures_probabilities.txt", sep = "")
sp_url = args$sigprob
cancer_signatures = read.table(sp_url, sep = "\t", header = TRUE)
# Match the order of the mutation types to MutationalPatterns standard
new_order = match(row.names(mutation_matrix), cancer_signatures$Somatic.Mutation.Type)
# Reorder cancer signatures dataframe
cancer_signatures = cancer_signatures[as.vector(new_order),]
# Add trinucletiode changes names as row.names
row.names(cancer_signatures) = cancer_signatures$Somatic.Mutation.Type
# Keep only 96 contributions of the signatures in matrix
cancer_signatures = as.matrix(cancer_signatures[,4:ncol(cancer_signatures)])
fit_res <- fit_to_signatures(mutation_matrix, cancer_signatures)
select <-(rowSums(fit_res$contribution) > 0)

# Get rid of "Signature." from signature name
sigs = gsub("([A-z])+([.])", "", rownames(fit_res$contribution))
contr = data.frame(sigs, fit_res$contribution)
colnames(contr) = c("Signature", sample_name)
write.table(contr, "contributions.tsv", sep="\t", quote=FALSE, row.names=FALSE)

pal = colorRampPalette(brewer.pal(11,"Spectral"))(ncol(cancer_signatures))[select]

png(filename="signature_contributions.png", type="cairo", width = 8, height = 6, units = 'in', res=600)
plot_contribution(
  fit_res$contribution[select,,drop = FALSE],
  cancer_signatures[,select,drop = FALSE],
  coord_flip = TRUE,
  mode = "absolute",
  palette = pal)
graphics.off()

maxview = max(mutation_matrix,fit_res$reconstructed)/sum(mutation_matrix)
png(filename="96_profiles.png", type="cairo", width = 10, height = 8, units = 'in', res=300)
plot_compare_profiles(
  mutation_matrix[,1],
  fit_res$reconstructed[,1],
  profile_names=c(sample_name,"Reconstructed"),
  profile_ymax = maxview,
  diff_ylim = c(-maxview/2, maxview/2),
  condensed = TRUE
)
graphics.off()

# source("https://bioconductor.org/biocLite.R")
# biocLite()
# biocLite("TxDb.Hsapiens.UCSC.hg19.knownGene")
suppressMessages(library("TxDb.Hsapiens.UCSC.hg19.knownGene"))
genes_hg19 = genes(TxDb.Hsapiens.UCSC.hg19.knownGene)
mut_mat_s = mut_matrix_stranded(vcfs, ref_genome, genes_hg19)
strand_counts = suppressMessages(strand_occurrences(mut_mat_s, by=sample_name))
strand_bias = suppressMessages(strand_bias_test(strand_counts))
strand_bias$group = sample_name

write.table(strand_counts, "strand_counts.tsv", sep="\t", quote=FALSE, row.names=FALSE)
write.table(strand_bias, "strand_bias.tsv", sep="\t", quote=FALSE, row.names=FALSE)

suppressMessages(library("gridExtra"))
ps1 = plot_strand(strand_counts, mode = "relative")
ps2 = suppressWarnings(plot_strand_bias(strand_bias))

png(filename="strand_bias.png", type="cairo", width = 8, height = 6, units = 'in', res=300)
grid.arrange(ps1, ps2)
graphics.off()
