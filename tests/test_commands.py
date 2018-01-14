"""Tests for click_signatures."""

import os

from click.testing import CliRunner

from click_signatures import __version__
from click_signatures import commands


def test_click_signatures(tmpdir):
    """Sample test for the main command."""
    runner = CliRunner()
    params = [
        "--outdir", str(tmpdir),
        "--id", os.environ["TEST_ID"],
        "--vcf", os.environ["TEST_VCF"],
        "--sigprob", os.environ["SIG_PROB"],
        "--Rscript", os.environ["RSCRIPT"]
        ]

    result = runner.invoke(commands.mutationalpatterns, params)
    assert result.exit_code == 0


def test_version():
    """Sample test for the __version__ variable."""
    assert __version__ == "0.1.0"
