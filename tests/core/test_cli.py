from click.testing import CliRunner

from core.cli import export_analysis

class TestCli:
    def test_export_analysis_help(self):
         runner = CliRunner()
         result = runner.invoke(export_analysis, ['--help'])
         assert result.exit_code == 0
         assert "Exports a template" in result.output
