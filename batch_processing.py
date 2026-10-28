import os
import glob
from dotenv import load_dotenv
from pypdf import PdfReader
from models import LossRunReport
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# 1. Load environment variables
load_dotenv()

# 2. Initialize LLM and Structured Output Chain
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.0
)
structured_llm = llm.with_structured_output(LossRunReport)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert P&C insurance document processing assistant. Extract structured loss run details accurately from the provided OCR text, regardless of layout variations."),
    ("user", "Extract the loss run report details from this document text:\n\n{document_text}")
])

chain = prompt | structured_llm

# 3. Setup output directory for JSON results
output_dir = "output_reports"
os.makedirs(output_dir, exist_ok=True)

# 4. Find all loss run PDFs in the directory automatically
pdf_files = glob.glob("loss_run_*.pdf")

if not pdf_files:
    print("⚠️ No loss run PDFs found starting with 'loss_run_'. Make sure your files are in the project folder!")
else:
    print(f"🚀 Found {len(pdf_files)} carrier PDF(s) to process. Starting batch pipeline...\n")

    for pdf_path in pdf_files:
        print(f"--------------------------------------------------")
        print(f"Processing: {pdf_path}")
        
        try:
            # Extract text
            reader = PdfReader(pdf_path)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text() + "\n"
            
            # Run through LangChain + Groq + Pydantic
            result = chain.invoke({"document_text": full_text})
            
            # Define output filename (e.g., loss_run_carrier_a_apex.pdf -> output_reports/loss_run_carrier_a_apex_structured.json)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            output_file_path = os.path.join(output_dir, f"{base_name}_structured.json")
            
            # Save to JSON
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(result.model_dump_json(indent=2))
                
            print(f"✅ Success! Saved structured report to: {output_file_path}")
            print(f"   - Insured: {result.insured_name}")
            print(f"   - Policy: {result.policy_number}")
            print(f"   - Claims Extracted: {len(result.claims)}")
            
        except Exception as e:
            print(f"❌ Error processing {pdf_path}: {e}")

    print(f"\n--------------------------------------------------")
    print("🎯 Batch processing complete! Check the 'output_reports' folder.")