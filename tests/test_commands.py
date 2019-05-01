from os.path import abspath
from os.path import dirname
from os.path import join

from click.testing import CliRunner

from click_signatures import cli

ROOT = abspath(dirname(__file__))

DATA = join(ROOT, "data")


def test_mutationpatterns(tmpdir):
    runner = CliRunner()
    params = [
        "--outdir",
        tmpdir,
        "--vcf",
        join(DATA, "test.vcf.gz"),
        "--id",
        "test",
        "--sigprob",
        join(DATA, "signatures_probabilities.txt"),
    ]
    result = runner.invoke(cli.main, params)

    assert result.exit_code == 0
