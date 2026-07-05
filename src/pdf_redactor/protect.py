from pathlib import Path
import secrets

import pikepdf
import typer


def protect_pdf(
    input_pdf: Path,
    output_pdf: Path,
    password: str,
) -> None:
    """Password-protect a PDF."""

    try:
        with pikepdf.open(input_pdf) as pdf:
            pdf.save(
                output_pdf,
                encryption=pikepdf.Encryption(
                    user=password,
                    owner=secrets.token_urlsafe(32),
                ),
            )

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