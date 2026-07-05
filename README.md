# pdf-redactor

Batch protect, unlock, and permanently redact sensitive information from PDF documents.

`pdf-redactor` is a command-line tool for processing multiple PDF files at once. It can password-protect PDFs, remove password protection, redact literal text or regular expression matches, and generate an audit report of everything it processed.

It was built for repetitive workflows where many documents contain the same confidential information and need to be sanitized quickly.

> **Note**
>
> This tool works with **text-based PDFs**. Scanned PDFs are images and require OCR before they can be searched or redacted.

---

## Features

- Password-protect PDF documents
- Remove password protection
- Batch process entire folders
- Redact literal text
- Redact using regular expressions
- Built-in presets (email, PAN, phone numbers, URLs, Aadhaar, IPv4)
- Custom pattern files
- TOML configuration support
- Dry-run mode
- JSON audit reports
- Rich CLI progress bar
- Continue processing even if one file fails
- Preserve original files

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/pdf-redactor.git
cd pdf-redactor
```

Create a virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the package:

```bash
pip install -e .
```

---

## Quick Start

Protect a PDF:

```bash
pdf-redactor protect document.pdf protected.pdf
```

Unlock a PDF:

```bash
pdf-redactor unlock protected.pdf unlocked.pdf
```

Redact every PDF inside a folder:

```bash
pdf-redactor redact input output \
    --password 1234 \
    --preset email \
    --preset pan
```

---

## Usage

### Protect a PDF

```bash
pdf-redactor protect input.pdf protected.pdf
```

---

### Unlock a PDF

```bash
pdf-redactor unlock protected.pdf unlocked.pdf
```

---

### Redact literal text

```bash
pdf-redactor redact input output \
    --password 1234 \
    --match "John Doe"
```

Multiple matches:

```bash
pdf-redactor redact input output \
    --password 1234 \
    --match "John Doe" \
    --match "Confidential"
```

---

### Redact using regex

```bash
pdf-redactor redact input output \
    --password 1234 \
    --regex "[A-Z]{5}[0-9]{4}[A-Z]"
```

Multiple regex patterns are supported.

---

### Use built-in presets

Instead of writing regex manually:

```bash
pdf-redactor redact input output \
    --password 1234 \
    --preset email \
    --preset phone \
    --preset pan
```

Available presets include:

- email
- phone
- pan
- aadhaar
- ipv4
- url

---

### Load matches from a file

`patterns.txt`

```text
John Doe
Confidential
Internal Use Only
```

Run:

```bash
pdf-redactor redact input output \
    --password 1234 \
    --match-file patterns.txt
```

---

### Configuration file

`company.toml`

```toml
presets = [
    "email",
    "pan",
]

matches = [
    "Confidential",
]

regexes = [
    "\\b\\d{10}\\b",
]
```

Run:

```bash
pdf-redactor redact input output \
    --password 1234 \
    --config company.toml
```

Command-line arguments and configuration can be combined.

---

### Dry run

Preview what would be redacted without modifying any files.

```bash
pdf-redactor redact input output \
    --password 1234 \
    --preset email \
    --dry-run
```

---

### JSON report

Generate a machine-readable report.

```bash
pdf-redactor redact input output \
    --password 1234 \
    --preset email \
    --report report.json
```

Example:

```json
{
  "summary": {
    "tool_version": "1.0.0",
    "generated_at": "2026-07-05T12:34:56+00:00",
    "pdfs_scanned": 5,
    "literal_hits": 8,
    "regex_hits": 21,
    "total_hits": 29,
    "dry_run": false
  },
  "files": [
    {
      "name": "invoice.pdf",
      "status": "success",
      "literal_hits": 2,
      "regex_hits": 5,
      "total_hits": 7
    }
  ]
}
```

---

## Project Structure

```text
pdf-redactor/

├── src/
│   └── pdf_redactor/
│       ├── cli.py
│       ├── config.py
│       ├── console.py
│       ├── presets.py
│       ├── protect.py
│       ├── redactor.py
│       └── unlock.py
│
├── tests/
├── examples/
├── pyproject.toml
└── README.md
```

---

## How It Works

1. Unlock the input PDF (if required).
2. Search every page for literal and/or regex matches.
3. Apply permanent PDF redactions.
4. Save the processed document.
5. Generate an optional JSON report.

---

## Limitations

- Works only with text-based PDFs.
- Does not perform OCR.
- Password-protected batch redaction assumes the input PDFs share the same password.
- Regex matches depend on the extracted text from the PDF.

---

## Testing

Run the test suite:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=pdf_redactor
```

---

## Why I Built This

I had a folder full of password-protected PDFs that all contained the same sensitive information. Unlocking and redacting them one by one was repetitive, so I wrote a small tool to automate the process.

It grew from a simple script into a reusable command-line utility that others might find useful too.

---

## License

MIT