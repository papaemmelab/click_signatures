"""click_signatures commands tests."""

import os

from click.testing import CliRunner

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
