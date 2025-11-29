import os
from pdf2image import convert_from_path
import pytesseract

# -----------------------------
# 1. PDF folder
# -----------------------------
PDF_FOLDER = r"C:\Users\saumy\OneDrive\Desktop\job\enhanced_pdfs"

# -----------------------------
# 2. Tesseract path (FIXED)
# -----------------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -----------------------------
# 3. Poppler path
# -----------------------------
POPPLER_PATH = r"C:\Users\saumy\OneDrive\Desktop\job\ors\pip\poppler-25.11.0\Library\bin"

# -----------------------------
# 4. Extract text function
# -----------------------------
def extract_text(pdf_path):
    print(f"\nProcessing: {pdf_path}")
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
    text_output = ""

    for i, page in enumerate(pages):
        print(f"  - OCR on page {i+1}")
        text = pytesseract.image_to_string(page)
        text_output += f"\n\n--- Page {i+1} ---\n{text}"

    return text_output

# -----------------------------
# 5. Process all PDFs
# -----------------------------
for file in os.listdir(PDF_FOLDER):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(PDF_FOLDER, file)
        text = extract_text(pdf_path)

        # Save OCR text to .txt file
        output_txt = pdf_path.replace(".pdf", ".txt")
        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved: {output_txt}")
