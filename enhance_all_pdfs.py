import os
import io
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
import img2pdf

INPUT_FOLDER = "pdfs"
OUTPUT_FOLDER = "enhanced_pdfs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def enhance_image_simple(img_pil):
    # Increase sharpness
    img_pil = ImageEnhance.Sharpness(img_pil).enhance(2.0)

    # Increase contrast
    img_pil = ImageEnhance.Contrast(img_pil).enhance(1.5)

    # Slight brightness boost
    img_pil = ImageEnhance.Brightness(img_pil).enhance(1.1)

    return img_pil


def enhance_pdf(input_path, output_path):
    print(f"Processing → {os.path.basename(input_path)}")

    # Convert PDF pages → list of PIL images
    pages = convert_from_path(input_path, dpi=300)

    enhanced_images_bytes = []

    for idx, img in enumerate(pages, 1):
        print(f" - Enhancing page {idx}")

        enhanced = enhance_image_simple(img)

        # Convert enhanced PIL image → bytes for img2pdf
        img_byte_arr = io.BytesIO()
        enhanced.save(img_byte_arr, format="JPEG")
        enhanced_images_bytes.append(img_byte_arr.getvalue())

    print(f" - Saving enhanced PDF → {output_path}")

    # Combine enhanced images into a single PDF
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(enhanced_images_bytes))

    print("   ✔ Done")


def process_all_pdfs():
    pdf_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".pdf")]
    if not pdf_files:
        print("❌ No PDFs found in folder:", INPUT_FOLDER)
        return

    for pdf in pdf_files:
        input_path = os.path.join(INPUT_FOLDER, pdf)
        output_path = os.path.join(OUTPUT_FOLDER, f"enhanced_{pdf}")
        enhance_pdf(input_path, output_path)

    print("\n🎉 All PDFs enhanced successfully!")


process_all_pdfs()
