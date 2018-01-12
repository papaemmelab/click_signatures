"""click_signatures pipeline."""

from os.path import abspath
from os.path import dirname
from os.path import join
import os
import subprocess
import tempfile

import click
import vcf as pyvcf

from click_signatures import validators

# This directory includes extra scripts required for the pipeline.
ETC_DIR = abspath(join(dirname(__file__), "etc"))


def makedirs(path, exist_ok=False):
    """Make dirs in python 2 does not support exist_ok flag."""
    if not os.path.exists(path):
        os.makedirs(path)


@click.command()
@click.option(
    "--outdir",
    type=click.Path(dir_okay=True, writable=True, resolve_path=True),
    required=True,
    help="Output Directory"
    )
@click.option(
    "--id", "sample_id",
    type=str,
    required=True,
    help="ID of Sample",
    )
@click.option(
    "--vcf",
    type=click.Path(file_okay=True, readable=True, resolve_path=True),
    required=True,
    help="SNP VCF File"
    )
@click.option(
    "--sigprob",
    type=click.Path(file_okay=True, readable=True, resolve_path=True),
    required=True,
    help="Signature Probrability File from Sanger"
    )
@click.option(
    "--Rscript",
    type=click.Path(file_okay=True, readable=True, resolve_path=True),
    default="Rscript",
    help="Rscript path (default: Rscript)"
    )
def mutationalpatterns(outdir, sample_id, vcf, sigprob, rscript):
    """Single Sample SNV mutation signature analysis (MutationalPatterns)."""
    makedirs(outdir, exist_ok=True)

    vcf_reader = pyvcf.Reader(filename=vcf)
    filtered_vcf = tempfile.NamedTemporaryFile()
    vcf_writer = pyvcf.Writer(filtered_vcf, vcf_reader)

    total = 0
    filtered = 0
    for record in vcf_reader:
        hasASRD = "ASRD" in record.INFO.keys()
        otherFILTER = True
        if hasASRD and record.INFO["ASRD"] < 0.95:
            otherFILTER = False
        if not record.FILTER and otherFILTER:
            vcf_writer.write_record(record)
            filtered += 1
        total += 1
    # Update tempfile but dont close/delete it
    vcf_writer.flush()

    click.echo("Total SNVs: " + str(total))
    click.echo("Passed SNVs: " + str(filtered))

    click.echo("Running R Mutational Patterns")

    cmd = [
        rscript,
        join(ETC_DIR, "mutationalpatterns.R"),
        "--outdir", outdir,
        "--id", sample_id,
        "--vcf", filtered_vcf.name,
        "--sigprob", sigprob
        ]

    click.echo(" ".join(cmd))
    subprocess.check_call(cmd)

    outputfiles = [
        "96_profiles.png", "context.tsv", "contributions.tsv",
        "signature_contributions.png", "strand_bias.png", "strand_bias.tsv",
        "strand_counts.tsv", "type_occurrences.png", "type_occurrences.tsv"
        ]

    outputfiles = [join(outdir, f) for f in outputfiles]

    click.echo("Checking output files")
    validators.check_patterns_are_files(outputfiles)
