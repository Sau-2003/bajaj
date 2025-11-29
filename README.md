# bajaj
1. PDF Enhancement (enhance_all_pdfs.py)
Converts low-quality scans into enhanced versions

Improves OCR accuracy

Output saved inside enhanced_pdfs/


2. OCR Text Extraction (ocr.py)
Converts enhanced PDFs → high-quality text

Handles multi-page invoices

Produces raw OCR text for further parsing


3. Layout & Table Detection (table_detection.py)
Identifies:

Table regions

Line-item rows

Numeric columns

Cleans and structures the extracted text


4. Data Aggregation & Summary (data_aggregation_summary.py)
Builds structured JSON:

Vendor details

All line items

Sub-totals

Final total

AI-computed total

Removes duplicate rows

Ensures completeness

