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
    matches: list[str] | None = typer.Option(
        [],
        "--match",
        "-m",
        help="Literal text to redact. Can be provided multiple times.",
    ),
):
    """Unlock PDFs and redact sensitive text."""

    run(
        input_folder=input_folder,
        output_folder=output_folder,
        pdf_password=password,
        matches=matches,
    )


if __name__ == "__main__":
    app()