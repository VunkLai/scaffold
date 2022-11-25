from click.testing import CliRunner

from scaffold.main import scaffold


def test_entrypoint():
    runner = CliRunner()
    result = runner.invoke(scaffold)
    assert result.exit_code == 0
    assert result.output.startswith("Usage: scaffold")
