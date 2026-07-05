PRESETS: dict[str, str] = {
    "email": r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
    "phone": r"\b\d{10}\b",
    "pan": r"[A-Z]{5}[0-9]{4}[A-Z]",
    "aadhaar": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
    "ipv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "url": r"https?://[^\s]+",
}