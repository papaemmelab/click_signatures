"""click_signatures cli tests."""

from click.testing import CliRunner

from click_signatures import cli


def test_cli():
    """Sample test for the main command."""
    runner = CliRunner()
    result = runner.invoke(cli.main, ["--help"])
    assert result.exit_code == 0
