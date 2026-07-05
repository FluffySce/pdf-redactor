from pathlib import Path

import typer

from pdf_redactor.protect import protect_pdf
from pdf_redactor.unlock import unlock_pdf
from pdf_redactor.redactor import run

app = typer.Typer(
    help="Protect, unlock and permanently redact PDF documents."
)


@app.callback()
def callback():
    """pdf-redactor CLI."""
    pass


@app.command()
def protect(
    input_pdf: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Input PDF to protect.",
    ),
    output_pdf: Path = typer.Argument(
        ...,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        help="Output protected PDF.",
    ),
    password: str = typer.Option(
        ...,
        "--password",
        "-p",
        prompt=True,
        hide_input=True,
        confirmation_prompt=True,
        help="Password to protect the PDF with.",
    ),
):
    """Password-protect a PDF."""

    protect_pdf(
        input_pdf=input_pdf,
        output_pdf=output_pdf,
        password=password,
    )


@app.command()
def unlock(
    input_pdf: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Protected PDF to unlock.",
    ),
    output_pdf: Path = typer.Argument(
        ...,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
        help="Unlocked output PDF.",
    ),
    password: str = typer.Option(
        ...,
        "--password",
        "-p",
        prompt=True,
        hide_input=True,
        help="Password used to unlock the PDF.",
    ),
):
    """Remove password protection from a PDF."""

    unlock_pdf(
        input_pdf=input_pdf,
        output_pdf=output_pdf,
        password=password,
    )


@app.command()
def redact(
    input_folder: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Directory containing password-protected PDFs.",
    ),
    output_folder: Path = typer.Argument(
        ...,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        help="Directory where processed PDFs will be written.",
    ),
    password: str = typer.Option(
        ...,
        "--password",
        "-p",
        prompt=True,
        hide_input=True,
        help="Password used to unlock all PDFs.",
    ),
    matches: list[str] = typer.Option(
        [],
        "--match",
        "-m",
        help="Literal text to redact. Can be specified multiple times.",
    ),
    regexes: list[str] = typer.Option(
        [],
        "--regex",
        "-r",
        help="Regex pattern to redact. Can be specified multiple times.",
    ),
    match_file: Path | None = typer.Option(
        None,
        "--match-file",
        "-f",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Text file containing one literal match per line.",
    ),
):
    """Unlock and redact PDFs."""

    all_matches = list(matches)

    if match_file:
        all_matches.extend(
            line.strip()
            for line in match_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )

    if not all_matches and not regexes:
        typer.echo(
            "Error: provide at least one --match, --match-file or --regex.",
            err=True,
        )
        raise typer.Exit(code=1)

    run(
        input_folder=input_folder,
        output_folder=output_folder,
        pdf_password=password,
        matches=all_matches,
        regexes=regexes,
    )


if __name__ == "__main__":
    app()