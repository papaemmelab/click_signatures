"""click_signatures pipeline."""

from os.path import abspath
from os.path import dirname
from os.path import join
import os
import subprocess
import tempfile

import click
from pysam import VariantFile

from click_signatures import __version__
from click_signatures import validators

# This directory includes extra scripts required for the pipeline.
DATA_DIR = abspath(join(dirname(__file__), "data"))


def makedirs(path, exist_ok=False):  # pylint: disable=unused-argument
    """Make dirs in python 2 does not support exist_ok flag."""
    if not os.path.exists(path):
        os.makedirs(path)


@click.command()
@click.version_option(version=__version__)
@click.option(
    "--outdir",
    type=click.Path(dir_okay=True, writable=True, resolve_path=True),
    required=True,
    help="Output Directory",
)
@click.option("--id", "sample_id", type=str, required=True, help="ID of Sample")
@click.option(
    "--vcf",
    type=click.Path(file_okay=True, readable=True, resolve_path=True),
    required=True,
    help="SNV VCF File",
)
@click.option(
    "--sigprob",
    type=click.Path(file_okay=True, readable=True, resolve_path=True),
    required=True,
    help="Signature Probrability File e.g. Sanger",
)
@click.option("--nofilter", is_flag=True, required=False, help="Dont filter VCF")
def mutationalpatterns(outdir, sample_id, vcf, sigprob, nofilter):
    """Single Sample SNV mutation signature analysis (MutationalPatterns)."""
    makedirs(outdir, exist_ok=True)

    total = 0
    filtered = 0
    vcf_reader = VariantFile(vcf, mode="r")
    filtered_vcf = tempfile.NamedTemporaryFile(mode="w")
    vcf_writer = VariantFile(filtered_vcf, mode="w", header=vcf_reader.header)

    for record in vcf_reader.fetch():
        total += 1

        if ("PASS" in list(record.filter) or not list(record.filter)) and not nofilter:
            vcf_writer.write(record)
            filtered += 1

    click.echo("Total SNVs: " + str(total))
    if not nofilter:
        click.echo("Passed SNVs: " + str(filtered))

    cmd = [
        "Rscript",
        join(DATA_DIR, "mutationalpatterns.R"),
        "--outdir",
        outdir,
        "--id",
        sample_id,
        "--vcf",
        vcf if nofilter else filtered_vcf.name,
        "--sigprob",
        sigprob,
    ]

    click.echo("Running R Mutational Patterns:%s" % " ".join(cmd))
    subprocess.check_call(cmd)

    # Check output files were generated.
    outputfiles = [
        "96_profiles.png",
        "context.tsv",
        "contributions.tsv",
        "signature_contributions.png",
        "strand_bias.png",
        "strand_bias.tsv",
        "strand_counts.tsv",
        "type_occurrences.png",
        "type_occurrences.tsv",
    ]

    outputfiles = [join(outdir, f) for f in outputfiles]
    validators.validate_patterns_are_files(outputfiles)
    click.echo("Output files OK.")
