from pathlib import Path

import pikepdf
import pytest
import typer

from pdf_redactor.protect import protect_pdf
from pdf_redactor.unlock import unlock_pdf


def test_unlock_creates_output(tmp_path: Path):
    input_pdf = Path("tests/assets/demo.pdf")

    protected_pdf = tmp_path / "protected.pdf"
    unlocked_pdf = tmp_path / "unlocked.pdf"

    protect_pdf(
        input_pdf=input_pdf,
        output_pdf=protected_pdf,
        password="1234",
    )

    unlock_pdf(
        input_pdf=protected_pdf,
        output_pdf=unlocked_pdf,
        password="1234",
    )

    assert unlocked_pdf.exists()


def test_unlocked_pdf_opens_without_password(tmp_path: Path):
    input_pdf = Path("tests/assets/demo.pdf")

    protected_pdf = tmp_path / "protected.pdf"
    unlocked_pdf = tmp_path / "unlocked.pdf"

    protect_pdf(
        input_pdf=input_pdf,
        output_pdf=protected_pdf,
        password="1234",
    )

    unlock_pdf(
        input_pdf=protected_pdf,
        output_pdf=unlocked_pdf,
        password="1234",
    )

    with pikepdf.open(unlocked_pdf) as pdf:
        assert len(pdf.pages) > 0


def test_wrong_password_raises_exit(tmp_path: Path):
    input_pdf = Path("tests/assets/demo.pdf")

    protected_pdf = tmp_path / "protected.pdf"
    unlocked_pdf = tmp_path / "unlocked.pdf"

    protect_pdf(
        input_pdf=input_pdf,
        output_pdf=protected_pdf,
        password="1234",
    )

    with pytest.raises(typer.Exit):
        unlock_pdf(
            input_pdf=protected_pdf,
            output_pdf=unlocked_pdf,
            password="wrong-password",
        )


def test_original_protected_pdf_is_unchanged(tmp_path: Path):
    input_pdf = Path("tests/assets/demo.pdf")

    protected_pdf = tmp_path / "protected.pdf"
    unlocked_pdf = tmp_path / "unlocked.pdf"

    protect_pdf(
        input_pdf=input_pdf,
        output_pdf=protected_pdf,
        password="1234",
    )

    original_size = protected_pdf.stat().st_size

    unlock_pdf(
        input_pdf=protected_pdf,
        output_pdf=unlocked_pdf,
        password="1234",
    )

    assert protected_pdf.stat().st_size == original_size