from pathlib import Path

import typer

from pdf_redactor.redactor import run

app = typer.Typer(
    help="Batch unlock password-protected PDFs and permanently redact sensitive text."
)


@app.callback()
def callback():
    """pdf-redactor CLI."""
    pass


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
        help="Literal text to redact. Can be provided multiple times.",
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
        help="Text file containing one match pattern per line.",

    )
):
    """Unlock PDFs and redact sensitive text."""

    all_matches = list(matches)
    if match_file:
        all_matches.extend(
            line.strip()
            for line in match_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    if not all_matches:
        typer.echo(
            "Error: Provide atleast one --match/-m or --match-file/-f .",
            err=True
        )
        raise typer.Exit(code=1)

    run(
        input_folder=input_folder,
        output_folder=output_folder,
        pdf_password=password,
        matches=all_matches,
    )


if __name__ == "__main__":
    app()