from pdf_redactor.presets import PRESETS


def test_email_exists():
    assert "email" in PRESETS


def test_pan_exists():
    assert "pan" in PRESETS


def test_phone_exists():
    assert "phone" in PRESETS


def test_url_exists():
    assert "url" in PRESETS


def test_aadhaar_exists():
    assert "aadhaar" in PRESETS


def test_presets_are_strings():
    for value in PRESETS.values():
        assert isinstance(value, str)