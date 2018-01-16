# click_signatures

This CLI performs single sample SNV mutational signature analysis using the R [MutationalPatterns][mutational] package.

# Table of Contents

<!-- This is for SublimeText's MarkdownTOC -->
<!-- MarkdownTOC autolink="true" bracket="round" depth=2 -->

- [Installation](#installation)
- [Usage](#usage)

<!-- /MarkdownTOC -->
# Installation

    pip install --editable .

# Usage

    click_signatures \
        --outdir {outdir} \
        --id {sample id} \
        --vcf {SNP vcf file} \
        --sigprob /ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/cosmic/signatures/signatures_probabilities.txt \
        --Rscript /ifs/work/leukgen/bin/R/3.4.3/bin/Rscript

<!-- references -->

[mutational]: https://github.com/UMCUGenetics/MutationalPatterns
