from pathlib import Path

import pikepdf
import typer


def unlock_pdf(
    input_pdf: Path,
    output_pdf: Path,
    password: str,
) -> None:
    """
    Remove password protection from a PDF.
    """

    try:
        with pikepdf.open(input_pdf, password=password) as pdf:
            pdf.save(output_pdf)

    except pikepdf.PasswordError:
        typer.echo(
            "Error: Incorrect PDF password.",
            err=True,
        )
        raise typer.Exit(code=1)

    except FileNotFoundError:
        typer.echo(
            f"Error: '{input_pdf}' not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    except Exception as e:
        typer.echo(
            f"Error: {e}",
            err=True,
        )
        raise typer.Exit(code=1)