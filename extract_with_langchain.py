import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from models import LossRunReport
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()

# 2. Initialize the ChatGroq model from LangChain
# We use openai/gpt-oss-120b for high accuracy on structured extraction
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.0
)

# 3. Bind our Pydantic schema directly to the model using LangChain's structured output
# This forces the LLM to return data matching our LossRunReport schema
structured_llm = llm.with_structured_output(LossRunReport)

# 4. Read the raw text from Carrier A's PDF
pdf_path = "loss_run_carrier_a_apex.pdf"
reader = PdfReader(pdf_path)
full_text = ""
for page in reader.pages:
    full_text += page.extract_text() + "\n"

print(f"--- Processing {pdf_path} using LangChain & Groq ---")

# 5. Create a professional prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert P&C insurance document processing assistant. Extract structured loss run details accurately from the provided OCR text."),
    ("user", "Extract the loss run report details from this document text:\n\n{document_text}")
])

# 6. Build the chain and invoke it
chain = prompt | structured_llm

result = chain.invoke({"document_text": full_text})

# 7. Print the final validated Pydantic model / JSON output
print("\n--- Production-Grade Extracted & Validated JSON ---")
print(result.model_dump_json(indent=2))