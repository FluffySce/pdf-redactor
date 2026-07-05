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
    input_folder: str = typer.Argument(
        ...,
        help="Directory containing password-protected PDFs.",
    ),
    output_folder: str = typer.Argument(
        ...,
        help="Directory where processed PDFs will be written.",
    ),
):
    """Unlock PDFs and redact sensitive text."""
    run(input_folder, output_folder)


if __name__ == "__main__":
    app()