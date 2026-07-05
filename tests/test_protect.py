from pathlib import Path

import pikepdf

from pdf_redactor.protect import protect_pdf


def test_protect_creates_output(tmp_path: Path):
    input_pdf = Path("tests/assets/demo.pdf")
    output_pdf = tmp_path / "protected.pdf"

    protect_pdf(
        input_pdf=input_pdf,
        output_pdf=output_pdf,
        password="1234",
    )

    assert output_pdf.exists()


def test_protected_pdf_requires_password(tmp_path: Path):
    input_pdf = Path("tests/assets/demo.pdf")
    output_pdf = tmp_path / "protected.pdf"

    protect_pdf(
        input_pdf=input_pdf,
        output_pdf=output_pdf,
        password="1234",
    )

    try:
        pikepdf.open(output_pdf)
        opened_without_password = True
    except pikepdf.PasswordError:
        opened_without_password = False

    assert opened_without_password is False


def test_protected_pdf_opens_with_password(tmp_path: Path):
    input_pdf = Path("tests/assets/demo.pdf")
    output_pdf = tmp_path / "protected.pdf"

    protect_pdf(
        input_pdf=input_pdf,
        output_pdf=output_pdf,
        password="1234",
    )

    with pikepdf.open(output_pdf, password="1234") as pdf:
        assert len(pdf.pages) > 0


def test_original_pdf_is_unchanged(tmp_path: Path):
    input_pdf = Path("tests/assets/demo.pdf")
    output_pdf = tmp_path / "protected.pdf"

    original_size = input_pdf.stat().st_size

    protect_pdf(
        input_pdf=input_pdf,
        output_pdf=output_pdf,
        password="1234",
    )

    assert input_pdf.stat().st_size == original_size