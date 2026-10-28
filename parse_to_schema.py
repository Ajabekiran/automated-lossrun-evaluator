from pypdf import PdfReader
from models import LossRunReport

pdf_path = "loss_run_carrier_a_apex.pdf"

# 1. Extract text from PDF
reader = PdfReader(pdf_path)
full_text = ""
for page in reader.pages:
    full_text += page.extract_text() + "\n"

print("--- Raw Text Extracted from PDF ---")
print(full_text[:300] + "...\n[Truncated for display]\n")

# 2. (Mocking the data mapping for now before we plug in the LLM)
# This shows how Pydantic wraps your raw extracted info into a clean object structure.
sample_structured_data = LossRunReport(
    insured_name="Apex Retail Logistics LLC",
    policy_number="APX-998234-2024",
    valuation_date="10/15/2026",
    claims=[
        {
            "claim_number": "CL-2024-01",
            "date_of_loss": "03/12/2024",
            "status": "Closed",
            "cause_description": "Property Damage - Warehouse pipe burst water damage",
            "paid_loss": "$42,500.00",
            "reserves": "$0.00",
            "total_incurred": "$42,500.00"
        }
    ]
)

print("--- Structured Pydantic Model Output ---")
print(sample_structured_data.model_dump_json(indent=2))