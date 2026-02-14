import os
import pikepdf
import fitz
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

PDF_PASSWORD = os.getenv("PDF_PASSWORD")
TEXT_TO_REDACT = os.getenv("TEXT_TO_REDACT")

INPUT_FOLDER = "protected_pdfs"
OUTPUT_FOLDER = "output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

for filename in os.listdir(INPUT_FOLDER):

    if not filename.endswith(".pdf"):
        continue

    input_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)
    temp_path = os.path.join(OUTPUT_FOLDER, "temp_unlocked.pdf")

    print(f"Processing: {filename}")

    # Step 1: unlock PDF
    with pikepdf.open(input_path, password=PDF_PASSWORD) as pdf:
        pdf.save(temp_path)

    # Step 2: redact text
    doc = fitz.open(temp_path)

    for page in doc:

        areas = page.search_for(TEXT_TO_REDACT)

        for area in areas:
            page.add_redact_annot(area, fill=(0, 0, 0))

        page.apply_redactions()

    doc.save(output_path)
    doc.close()

# cleanup temp file
if os.path.exists(temp_path):
    os.remove(temp_path)

print("Done. All PDFs unlocked and redacted.")
