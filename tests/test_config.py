from pathlib import Path

import pytest
import typer

from pdf_redactor.config import load_config


def test_load_valid_config(tmp_path: Path):
    config = tmp_path / "config.toml"

    config.write_text(
        """
presets = ["email", "pan"]

matches = [
    "Confidential",
]

regexes = [
    "\\\\b\\\\d{10}\\\\b",
]
""",
        encoding="utf-8",
    )

    data = load_config(config)

    assert data["presets"] == ["email", "pan"]
    assert data["matches"] == ["Confidential"]
    assert data["regexes"] == [r"\b\d{10}\b"]


def test_missing_config_file():
    with pytest.raises(typer.Exit):
        load_config(Path("does-not-exist.toml"))


def test_invalid_toml(tmp_path: Path):
    config = tmp_path / "broken.toml"

    config.write_text(
        "presets = [",
        encoding="utf-8",
    )

    with pytest.raises(typer.Exit):
        load_config(config)