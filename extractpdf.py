from pypdf import PdfReader

# We will start by testing Carrier A's document
pdf_path = "loss_run_carrier_a_apex.pdf"

print(f"Reading file: {pdf_path}...\n")

# Read the PDF
reader = PdfReader(pdf_path)
full_text = ""

# Loop through each page and extract text
for index, page in enumerate(reader.pages):
    print(f"--- Page {index + 1} ---")
    page_text = page.extract_text()
    print(page_text)
    full_text += page_text + "\n"

print("\n--- Extraction Successful! ---")