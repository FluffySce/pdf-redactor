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
def redact():
    """Unlock PDFs and redact sensitive text."""
    run()


if __name__ == "__main__":
    app()