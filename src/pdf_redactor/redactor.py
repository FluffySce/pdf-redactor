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
    dry_run: bool,
) -> dict:
    output_folder.mkdir(parents=True, exist_ok=True)

    temp_path = output_folder / "temp_unlocked.pdf"

    total_files = 0
    total_literal_hits = 0
    total_regex_hits = 0

    files: list[dict] = []

    try:
        compiled_regexes = [
            re.compile(pattern)
            for pattern in regexes
        ]
    except re.error as e:
        typer.echo(f"Invalid regex: {e}", err=True)
        raise typer.Exit(code=1)

    try:
        for pdf in input_folder.iterdir():

            if pdf.suffix.lower() != ".pdf":
                continue

            total_files += 1

            typer.echo(f"Processing: {pdf.name}")

            output_path = output_folder / pdf.name

            unlock_pdf(
                input_pdf=pdf,
                output_pdf=temp_path,
                password=pdf_password,
            )

            doc = fitz.open(temp_path)

            file_literal_hits = 0
            file_regex_hits = 0

            for page in doc:

                # Literal matches
                for match in matches:

                    for area in page.search_for(match):

                        file_literal_hits += 1

                        if not dry_run:
                            page.add_redact_annot(
                                area,
                                fill=(0, 0, 0),
                            )

                # Regex matches
                page_text = page.get_text()

                for compiled in compiled_regexes:

                    for regex_match in compiled.finditer(page_text):

                        matched_text = regex_match.group(0)

                        for area in page.search_for(matched_text):

                            file_regex_hits += 1

                            if not dry_run:
                                page.add_redact_annot(
                                    area,
                                    fill=(0, 0, 0),
                                )

                if not dry_run:
                    page.apply_redactions()

            if not dry_run:
                doc.save(output_path)

            doc.close()

            total_literal_hits += file_literal_hits
            total_regex_hits += file_regex_hits

            files.append(
                {
                    "name": pdf.name,
                    "literal_hits": file_literal_hits,
                    "regex_hits": file_regex_hits,
                    "total_hits": (
                        file_literal_hits
                        + file_regex_hits
                    ),
                }
            )

    finally:
        if temp_path.exists():
            temp_path.unlink()

    return {
        "summary": {
            "pdfs_scanned": total_files,
            "literal_hits": total_literal_hits,
            "regex_hits": total_regex_hits,
            "total_hits": (
                total_literal_hits
                + total_regex_hits
            ),
            "dry_run": dry_run,
        },
        "files": files,
    }