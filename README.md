# PDF Password Remover & Bulk Redactor

A secure Python tool to remove passwords from multiple PDF files and permanently redact specific sensitive text across all documents.

This tool is designed for batch processing where multiple PDFs share the same password and contain identical confidential information that must be removed safely and automatically.

---

## Features

- Remove password protection from PDFs in bulk
- Permanently redact specific text from all PDFs
- Batch processing with zero manual work
- Secure handling of secrets using environment variables
- Safe GitHub workflow (no passwords or sensitive data exposed)
- Fast, lightweight, and fully automated

---

## Tech Stack

- Python 3.8+
- pikepdf (PDF password removal)
- PyMuPDF / fitz (PDF text search and redaction)
- python-dotenv (secure secret management)

---

## Project Structure

```
pdf-redactor/
│
├── protected_pdfs/       # Input PDFs (ignored by Git)
├── output/               # Output PDFs (ignored by Git)
│
├── main.py               # Main script
├── requirements.txt
├── .env.example         # Environment variable template
├── .gitignore
└── README.md
```

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/yourusername/pdf-redactor.git
cd pdf-redactor
```

### 2. Create virtual environment

Windows:

```
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```
python -m venv venv
source venv/bin/activate
```

---

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file in the project root:

```
PDF_PASSWORD=your_pdf_password
TEXT_TO_REDACT=exact text to remove
```

Example:

```
PDF_PASSWORD=abc123
TEXT_TO_REDACT=PAN: ABCDE1234F
```

Do NOT upload `.env` to GitHub.

---

## Usage

### Step 1: Place PDFs into

```
protected_pdfs/
```

### Step 2: Run the script

```
python main.py
```

---

## Output

Processed files will appear in:

```
output/
```

Original files remain unchanged.

---

## Security

Sensitive information is stored in environment variables, not in source code.

Ignored by Git:

```
.env
protected_pdfs/
output/
venv/
```

---

## How It Works

1. Opens password-protected PDFs using pikepdf
2. Saves unlocked temporary copies
3. Searches for target text using PyMuPDF
4. Permanently redacts the text
5. Saves clean output PDFs

Redaction is permanent and cannot be reversed.

---

## Requirements

- Python 3.8+
- Selectable text PDFs (not scanned images)

---

## License

MIT License

---

## Disclaimer

Use responsibly. Ensure you have permission to modify and redact documents.
