import os
import json
from collections import defaultdict

# ----------------------------------------------------------
# Folder containing *_extracted.json files
# ----------------------------------------------------------
JSON_FOLDER = r"C:\Users\saumy\OneDrive\Desktop\job\enhanced_pdfs"

# ----------------------------------------------------------
# 1. Aggregation & API Response Function
# ----------------------------------------------------------
def generate_api_response():
    invoice_files = [f for f in os.listdir(JSON_FOLDER) if f.endswith("_extracted.json")]
    if not invoice_files:
        print("❌ No extracted JSON files found in:", JSON_FOLDER)
        return

    total_tokens_dummy = 0  # You can replace with real LLM token counts if used

    response_data = {
        "is_success": True,
        "token_usage": {
            "total_tokens": total_tokens_dummy,
            "input_tokens": total_tokens_dummy,
            "output_tokens": total_tokens_dummy
        },
        "data": {
            "pagewise_line_items": [],
            "total_item_count": 0
        }
    }

    total_items_count = 0

    for file in invoice_files:
        file_path = os.path.join(JSON_FOLDER, file)

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        pages = data.get("pages", [])  # Assuming your extracted JSON has page-wise info
        for page in pages:
            page_no = str(page.get("page_no", "1"))
            page_type = page.get("page_type", "Bill Detail")

            bill_items_list = []
            for item in page.get("line_items", []):
                try:
                    bill_items_list.append({
                        "item_name": item.get("description", ""),
                        "item_amount": float(item.get("amount", 0)),
                        "item_rate": float(item.get("rate", 0)),
                        "item_quantity": float(item.get("quantity", 1))
                    })
                    total_items_count += 1
                except:
                    continue  # Skip malformed items

            response_data["data"]["pagewise_line_items"].append({
                "page_no": page_no,
                "page_type": page_type,
                "bill_items": bill_items_list
            })

    response_data["data"]["total_item_count"] = total_items_count
    return response_data

# ----------------------------------------------------------
# 2. Save API Response JSON
# ----------------------------------------------------------
def save_api_response():
    response = generate_api_response()
    if not response:
        return

    out_path = os.path.join(JSON_FOLDER, "API_RESPONSE.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(response, f, indent=4)

    print("\n✅ API-style Response Saved →", out_path)


# Run
if __name__ == "__main__":
    save_api_response()
