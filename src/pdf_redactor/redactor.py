from pathlib import Path
import re

import fitz
import typer

from pdf_redactor.unlock import unlock_pdf


def redact_pdfs(
    input_folder: Path,
    output_folder: Path,
    pdf_password: str,
    matches: list[str],
    regexes: list[str],
) -> None:
    output_folder.mkdir(parents=True, exist_ok=True)

    temp_path = output_folder / "temp_unlocked.pdf"

    # Compile regexes once
    try:
        compiled_regexes = [re.compile(pattern) for pattern in regexes]
    except re.error as e:
        typer.echo(f"Invalid regex: {e}", err=True)
        raise typer.Exit(code=1)

    try:
        for pdf in input_folder.iterdir():
            if pdf.suffix.lower() != ".pdf":
                continue

            typer.echo(f"Processing: {pdf.name}")

            output_path = output_folder / pdf.name

            # Unlock the PDF using the shared helper
            unlock_pdf(
                input_pdf=pdf,
                output_pdf=temp_path,
                password=pdf_password,
            )

            # Open the unlocked PDF
            doc = fitz.open(temp_path)

            for page in doc:

                # Literal matches
                for match in matches:
                    for area in page.search_for(match):
                        page.add_redact_annot(area, fill=(0, 0, 0))

                # Regex matches
                page_text = page.get_text()

                for compiled in compiled_regexes:
                    for regex_match in compiled.finditer(page_text):
                        matched_text = regex_match.group(0)

                        # Locate matched text on the page
                        for area in page.search_for(matched_text):
                            page.add_redact_annot(area, fill=(0, 0, 0))

                # Apply all queued redactions
                page.apply_redactions()

            doc.save(output_path)
            doc.close()

    finally:
        if temp_path.exists():
            temp_path.unlink()

    typer.echo("Done. All PDFs unlocked and redacted.")