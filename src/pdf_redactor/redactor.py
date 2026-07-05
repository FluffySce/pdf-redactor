import os

import fitz
import pikepdf
import typer
from dotenv import load_dotenv

def run(
    input_folder: str,
    output_folder: str,
):
    load_dotenv(".env")

    pdf_password = os.getenv("PDF_PASSWORD")
    text_to_redact = os.getenv("TEXT_TO_REDACT")

    os.makedirs(output_folder, exist_ok=True)

    if not os.path.isdir(input_folder):
        typer.echo(
            f"Error: '{input_folder}' directory not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    temp_path = os.path.join(output_folder, "temp_unlocked.pdf")

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(".pdf"):
            continue

        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)

        typer.echo(f"Processing: {filename}")

        # Step 1: Unlock PDF
        with pikepdf.open(input_path, password=pdf_password) as pdf:
            pdf.save(temp_path)

        # Step 2: Redact text
        doc = fitz.open(temp_path)

        for page in doc:
            areas = page.search_for(text_to_redact)

            for area in areas:
                page.add_redact_annot(area, fill=(0, 0, 0))

            page.apply_redactions()

        doc.save(output_path)
        doc.close()

    if os.path.exists(temp_path):
        os.remove(temp_path)

    typer.echo("Done. All PDFs unlocked and redacted.")