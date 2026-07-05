from datetime import UTC, datetime
from pathlib import Path
import re

import fitz
import typer
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)

from pdf_redactor.console import console
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
        console.print(f"[red]Invalid regex:[/red] {e}")
        raise typer.Exit(code=1)

    pdfs = [
        pdf
        for pdf in input_folder.iterdir()
        if pdf.suffix.lower() == ".pdf"
    ]

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
            console=console,
            transient=True,
        ) as progress:

            task = progress.add_task(
                "Redacting PDFs",
                total=len(pdfs),
            )

            for pdf in pdfs:

                progress.update(
                    task,
                    description=f"[cyan]Processing[/cyan] {pdf.name}",
                )

                total_files += 1

                output_path = output_folder / pdf.name

                file_literal_hits = 0
                file_regex_hits = 0

                try:
                    unlock_pdf(
                        input_pdf=pdf,
                        output_pdf=temp_path,
                        password=pdf_password,
                    )

                    doc = fitz.open(temp_path)

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
                            "status": "success",
                            "literal_hits": file_literal_hits,
                            "regex_hits": file_regex_hits,
                            "total_hits": (
                                file_literal_hits
                                + file_regex_hits
                            ),
                        }
                    )

                    progress.update(
                        task,
                        description=f"[green]✓[/green] {pdf.name}",
                    )

                except Exception as e:

                    files.append(
                        {
                            "name": pdf.name,
                            "status": "failed",
                            "error": str(e),
                            "literal_hits": file_literal_hits,
                            "regex_hits": file_regex_hits,
                            "total_hits": (
                                file_literal_hits
                                + file_regex_hits
                            ),
                        }
                    )

                    progress.update(
                        task,
                        description=f"[red]✗[/red] {pdf.name}",
                    )

                finally:
                    progress.advance(task)

    finally:
        if temp_path.exists():
            temp_path.unlink()

    return {
        "summary": {
            "tool_version": "1.0.0",
            "generated_at": (
                datetime.now(UTC)
                .replace(microsecond=0)
                .isoformat()
            ),
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