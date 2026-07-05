from pathlib import Path
import tomllib
import typer


def load_config(path: Path) -> dict:
    """
    Load a TOML configuration file.
    """

    try:
        with path.open("rb") as f:
            config = tomllib.load(f)

    except FileNotFoundError:
        typer.echo(f"Error: Config file '{path}' not found.", err=True)
        raise typer.Exit(code=1)

    except tomllib.TOMLDecodeError as e:
        typer.echo(f"Invalid TOML: {e}", err=True)
        raise typer.Exit(code=1)

    return config