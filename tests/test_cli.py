from pathlib import Path

from typer.testing import CliRunner

from pdf_redactor.cli import app

runner = CliRunner()


def test_help():
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "Protect" in result.stdout
    assert "Unlock" in result.stdout


def test_redact_help():
    result = runner.invoke(app, ["redact", "--help"])

    assert result.exit_code == 0
    assert "--match" in result.stdout
    assert "--regex" in result.stdout
    assert "--preset" in result.stdout
    assert "--config" in result.stdout


def test_unlock_help():
    result = runner.invoke(app, ["unlock", "--help"])

    assert result.exit_code == 0


def test_protect_help():
    result = runner.invoke(app, ["protect", "--help"])

    assert result.exit_code == 0


def test_invalid_preset(tmp_path: Path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"

    input_dir.mkdir()
    output_dir.mkdir()

    result = runner.invoke(
        app,
        [
            "redact",
            str(input_dir),
            str(output_dir),
            "--password",
            "1234",
            "--preset",
            "definitely-not-a-real-preset",
        ],
    )

    assert result.exit_code != 0
    assert "Unknown preset" in result.output


def test_missing_match_options(tmp_path: Path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"

    input_dir.mkdir()
    output_dir.mkdir()

    result = runner.invoke(
        app,
        [
            "redact",
            str(input_dir),
            str(output_dir),
            "--password",
            "1234",
        ],
    )

    assert result.exit_code != 0
    assert "provide at least one" in result.output.lower()