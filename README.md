# 🛡️ Intelligent P&C Insurance Loss Run Underwriting & SOP Engine

A production-grade, end-to-end GenAI pipeline designed to automate Commercial Property & Casualty (P&C) insurance loss run document processing, data standardization, and underwriting compliance adjudication.

---

## 🚀 Business Problem & Impact
Commercial insurance underwriting relies heavily on reviewing historical "loss run" reports from various carrier portals. Because every carrier uses a completely different layout and format, manual data extraction is tedious, error-prone, and creates massive underwriting bottlenecks. 

This system automates the entire intake-to-decision workflow:
1. **Ingests** unstructured carrier PDFs regardless of layout variations.
2. **Extracts & Structures** raw text into strict, type-safe JSON contracts using LLMs and Pydantic.
3. **Validates Compliance** against custom carrier Standard Operating Procedures (SOPs) to instantly triage submissions into *Auto-Approved*, *Warnings*, or *Referral / Decline*.

---

## 🏗️ Architecture & Tech Stack

* **Language:** Python 3.10+
* **Orchestration:** LangChain (`ChatPromptTemplate`, `with_structured_output`)
* **LLM Inference:** Groq API (`openai/gpt-oss-120b` for ultra-fast, high-accuracy structured reasoning)
* **Data Validation & Contracts:** Pydantic V2
* **Document Ingestion:** `pypdf`
* **Configuration:** `python-dotenv`

---

## 📂 Project Structure

```text
├── output_reports/             # Exported structured JSON data
├── models.py                   # Pydantic data contracts (ClaimItem & LossRunReport)
├── batch_processing.py         # Multi-carrier PDF text extraction and LLM parsing pipeline
├── validate_sop.py             # Automated Underwriting Rules Engine (SOP compliance)
├── requirements.txt            # Project dependencies
└── .env.example                # Environment variable template