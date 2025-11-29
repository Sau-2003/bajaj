import os
from pdf2image import convert_from_path
import layoutparser as lp
from PIL import Image

# -----------------------------
# 1. PDF folder
# -----------------------------
PDF_FOLDER = r"C:\Users\saumy\OneDrive\Desktop\job\enhanced_pdfs"

# -----------------------------
# 2. Poppler path
# -----------------------------
POPPLER_PATH = r"C:\Users\saumy\OneDrive\Desktop\job\ors\pip\poppler-25.11.0\Library\bin"

# -----------------------------
# 3. Layout Detection Model
# -----------------------------
model = lp.Detectron2LayoutModel(
    'lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config',
    extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5],
    label_map={0: "Text", 1: "Title", 2: "List", 3: "Table", 4: "Figure"}
)

# -----------------------------
# 4. Layout Analysis & Table Detection Function
# -----------------------------
def detect_layout(pdf_path):
    print(f"\nProcessing: {pdf_path}")
    pages = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
    
    for i, page in enumerate(pages):
        print(f"  - Analyzing page {i+1}")
        # Convert PIL page to OpenCV image
        page_cv = lp.io.pil_to_cv2(page)

        # Detect layout
        layout = model.detect(page_cv)

        # Save layout visualization
        layout_image = lp.draw_box(
            page_cv,
            layout,
            box_width=3,
            show_element_type=True
        )
        layout_img_path = pdf_path.replace(".pdf", f"_page{i+1}_layout.png")
        Image.fromarray(layout_image).save(layout_img_path)
        print(f"    Saved layout image: {layout_img_path}")

        # Print detected blocks
        for block in layout:
            print(f"    {block.type} - {block.coordinates}")

# -----------------------------
# 5. Process all PDFs
# -----------------------------
for file in os.listdir(PDF_FOLDER):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(PDF_FOLDER, file)
        detect_layout(pdf_path)
