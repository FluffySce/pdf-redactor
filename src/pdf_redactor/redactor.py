from pathlib import Path

import fitz
import pikepdf
import typer


def run(
    input_folder: Path,
    output_folder: Path,
    pdf_password: str,
    matches: list[str],
) -> None:
    output_folder.mkdir(parents=True, exist_ok=True)

    temp_path = output_folder / "temp_unlocked.pdf"

    try:
        for pdf in input_folder.iterdir():
            if pdf.suffix.lower() != ".pdf":
                continue

            typer.echo(f"Processing: {pdf.name}")

            output_path = output_folder / pdf.name

            # Step 1: Unlock PDF
            with pikepdf.open(pdf, password=pdf_password) as unlocked_pdf:
                unlocked_pdf.save(temp_path)

            # Step 2: Redact text
            doc = fitz.open(temp_path)

            for page in doc:
                for match in matches:
                    areas = page.search_for(match)

                    for area in areas:
                        page.add_redact_annot(area, fill=(0, 0, 0))

                page.apply_redactions()

            doc.save(output_path)
            doc.close()

    finally:
        if temp_path.exists():
            temp_path.unlink()

    typer.echo("Done. All PDFs unlocked and redacted.")