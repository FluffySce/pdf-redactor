from pathlib import Path

import pytest
import typer

from pdf_redactor.protect import protect_pdf
from pdf_redactor.redactor import redact_pdfs


PASSWORD = "1234"


def prepare_input(tmp_path: Path) -> Path:
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    protect_pdf(
        input_pdf=Path("tests/assets/demo.pdf"),
        output_pdf=input_dir / "demo.pdf",
        password=PASSWORD,
    )

    return input_dir


def test_redactor_returns_report(tmp_path: Path):
    input_dir = prepare_input(tmp_path)
    output_dir = tmp_path / "output"

    report = redact_pdfs(
        input_folder=input_dir,
        output_folder=output_dir,
        pdf_password=PASSWORD,
        matches=["Hello World"],
        regexes=[],
        dry_run=True,
    )

    assert isinstance(report, dict)
    assert "summary" in report
    assert "files" in report


def test_dry_run_creates_no_output_pdf(tmp_path: Path):
    input_dir = prepare_input(tmp_path)
    output_dir = tmp_path / "output"

    redact_pdfs(
        input_folder=input_dir,
        output_folder=output_dir,
        pdf_password=PASSWORD,
        matches=["Hello"],
        regexes=[],
        dry_run=True,
    )

    assert not (output_dir / "demo.pdf").exists()


def test_normal_run_creates_output_pdf(tmp_path: Path):
    input_dir = prepare_input(tmp_path)
    output_dir = tmp_path / "output"

    redact_pdfs(
        input_folder=input_dir,
        output_folder=output_dir,
        pdf_password=PASSWORD,
        matches=["Hello"],
        regexes=[],
        dry_run=False,
    )

    assert (output_dir / "demo.pdf").exists()


def test_invalid_regex_raises(tmp_path: Path):
    input_dir = prepare_input(tmp_path)
    output_dir = tmp_path / "output"

    with pytest.raises(typer.Exit):
        redact_pdfs(
            input_folder=input_dir,
            output_folder=output_dir,
            pdf_password=PASSWORD,
            matches=[],
            regexes=["["],
            dry_run=True,
        )


def test_summary_contains_expected_keys(tmp_path: Path):
    input_dir = prepare_input(tmp_path)
    output_dir = tmp_path / "output"

    report = redact_pdfs(
        input_folder=input_dir,
        output_folder=output_dir,
        pdf_password=PASSWORD,
        matches=["Hello"],
        regexes=[],
        dry_run=True,
    )

    summary = report["summary"]

    assert "tool_version" in summary
    assert "generated_at" in summary
    assert "pdfs_scanned" in summary
    assert "literal_hits" in summary
    assert "regex_hits" in summary
    assert "total_hits" in summary
    assert "dry_run" in summary


def test_file_entry_contains_expected_keys(tmp_path: Path):
    input_dir = prepare_input(tmp_path)
    output_dir = tmp_path / "output"

    report = redact_pdfs(
        input_folder=input_dir,
        output_folder=output_dir,
        pdf_password=PASSWORD,
        matches=["Hello"],
        regexes=[],
        dry_run=True,
    )

    file = report["files"][0]

    assert "name" in file
    assert "status" in file
    assert "literal_hits" in file
    assert "regex_hits" in file
    assert "total_hits" in file


def test_empty_folder(tmp_path: Path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    output_dir = tmp_path / "output"

    report = redact_pdfs(
        input_folder=input_dir,
        output_folder=output_dir,
        pdf_password=PASSWORD,
        matches=["Hello"],
        regexes=[],
        dry_run=True,
    )

    assert report["summary"]["pdfs_scanned"] == 0