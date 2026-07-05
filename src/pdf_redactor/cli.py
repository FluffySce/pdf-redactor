from pathlib import Path

import typer
import click
import json

from pdf_redactor.presets import PRESETS
from pdf_redactor.protect import protect_pdf
from pdf_redactor.redactor import redact_pdfs
from pdf_redactor.unlock import unlock_pdf
from click.shell_completion import CompletionItem
from pdf_redactor.config import load_config


app = typer.Typer(
    help="Protect, unlock and permanently redact PDF documents."
)

def complete_presets(
    ctx: click.Context,
    param: click.Parameter,
    incomplete: str,
):
    return [
        CompletionItem(preset)
        for preset in PRESETS
        if preset.startswith(incomplete.lower())
    ]


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

    typer.echo(f"Protected PDF written to '{output_pdf}'.")


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

    typer.echo(f"Unlocked PDF written to '{output_pdf}'.")


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
        help="Regular expression to redact. Can be specified multiple times.",
    ),
    presets: list[str] = typer.Option(
        [],
        "--preset",
        help="Built-in preset(s). Can be specified multiple times.",
        shell_complete=complete_presets,
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
    config: Path | None = typer.Option(
        None,
        "--config",
        "-c",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="TOML configuration file.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show what would be redacted without modifying PDFs.",
    ),
    report_file: Path | None = typer.Option(
        None,
        "--report",
        help="Write execution report to a JSON file."
    ),
):
    """Unlock and redact PDFs."""

    all_matches = list(matches)
    all_regexes = list(regexes)
    
    if config:
        cfg = load_config(config)

        all_matches.extend(cfg.get("matches", []))
        all_regexes.extend(cfg.get("regexes", []))

        for preset in cfg.get("presets", []):
            key = preset.lower()

            if key not in PRESETS:
                typer.echo(
                    f"Unknown preset '{preset}' in config.",
                    err=True,
                )
                raise typer.Exit(code=1)

            all_regexes.append(PRESETS[key])

    # Load literal matches from file
    if match_file:
        all_matches.extend(
            line.strip()
            for line in match_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )

    # Resolve presets
    for preset in presets:
        key = preset.lower()

        if key not in PRESETS:
            typer.echo(
                f"Unknown preset '{preset}'.",
                err=True,
            )
            typer.echo(
                f"Available presets: {', '.join(sorted(PRESETS))}",
                err=True,
            )
            raise typer.Exit(code=1)

        all_regexes.append(PRESETS[key])

    if not all_matches and not all_regexes:
        typer.echo(
            "Error: provide at least one --match, --match-file, --regex or --preset.",
            err=True,
        )
        raise typer.Exit(code=1)

    report = redact_pdfs(
        input_folder=input_folder,
        output_folder=output_folder,
        pdf_password=password,
        matches=all_matches,
        regexes=all_regexes,
        dry_run=dry_run,
    )

    summary = report["summary"]

    typer.echo()

    for file in report["files"]:
        typer.echo(file["name"])
        typer.echo("-" * len(file["name"]))
        typer.echo(f"Literal hits : {file['literal_hits']}")
        typer.echo(f"Regex hits   : {file['regex_hits']}")
        typer.echo(f"Total hits   : {file['total_hits']}")
        typer.echo()

    if summary["dry_run"]:
        typer.echo("Dry run complete.")
        typer.echo("No PDFs were modified.")
    else:
        typer.echo("Done. All PDFs unlocked and redacted.")

    typer.echo()
    typer.echo("Overall Summary")
    typer.echo("---------------")
    typer.echo(f"PDFs scanned : {summary['pdfs_scanned']}")
    typer.echo(f"Literal hits : {summary['literal_hits']}")
    typer.echo(f"Regex hits   : {summary['regex_hits']}")
    typer.echo(f"Total hits   : {summary['total_hits']}")

    if report_file:
        report_file.write_text(
            json.dumps(report, indent=2),
            encoding="utf-8",
        )
        typer.echo()
        typer.echo(f"Report written to '{report_file}'.")


if __name__ == "__main__":
    app()