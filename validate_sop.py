import os
import glob
import json
from models import LossRunReport

def evaluate_sop_compliance(report: LossRunReport) -> dict:
    """
    Evaluates an insurance loss run report against hypothetical carrier SOP guidelines:
    1. Open Claims Rule: Max 1 open claim allowed without referral.
    2. Large Loss Rule: No single claim can have a total incurred amount > $50,000.
    3. Data Completeness: Valuation date and policy number must be present.
    """
    violations = []
    warnings = []
    
    # Clean up currency strings for numerical comparison (e.g., "$42,500.00" -> 42500.0)
    def parse_currency(curr_str: str) -> float:
        try:
            return float(curr_str.replace("$", "").replace(",", "").strip())
        except ValueError:
            return 0.0

    # 1. Check Data Completeness
    if not report.policy_number or report.policy_number.lower() == "unknown":
        violations.append("Critical: Missing or invalid policy number.")
    if not report.valuation_date:
        warnings.append("Warning: Valuation date is missing.")

    # 2. Analyze Individual Claims
    open_claims_count = 0
    for claim in report.claims:
        # Check Claim Status
        if claim.status.lower() in ["open", "pending"]:
            open_claims_count += 1
            
        # Check Large Loss Threshold ($50,000 limit)
        total_incurred_val = parse_currency(claim.total_incurred)
        if total_incurred_val > 50000.0:
            violations.append(f"SOP Violation: Claim {claim.claim_number} exceeds large loss threshold ($50k) with {claim.total_incurred}.")

    # 3. Check Open Claims Threshold (Max 1 allowed)
    if open_claims_count > 1:
        violations.append(f"SOP Violation: Portfolio has {open_claims_count} open claims (Maximum allowed is 1).")

    # Determine Underwriting Decision
    if violations:
        decision = "REFERRAL / DECLINE (SOP Breached)"
    elif warnings:
        decision = "REFER WITH WARNINGS"
    else:
        decision = "AUTO-APPROVED (Clean Submission)"

    return {
        "decision": decision,
        "violations": violations,
        "warnings": warnings,
        "open_claims_count": open_claims_count,
        "total_claims_evaluated": len(report.claims)
    }

def run_compliance_pipeline():
    output_dir = "output_reports"
    json_files = glob.glob(os.path.join(output_dir, "*_structured.json"))

    if not json_files:
        print(f"⚠️ No structured JSON reports found in '{output_dir}/'. Run batch_process.py first!")
        return

    print(f"🛡️ Running Underwriting SOP Compliance Engine on {len(json_files)} report(s)...\n")

    for file_path in json_files:
        print(f"--------------------------------------------------")
        print(f"Evaluating Report: {os.path.basename(file_path)}")
        
        try:
            # Read and validate JSON back into our Pydantic model
            with open(file_path, "r", encoding="utf-8") as f:
                json_data = f.read()
            
            report = LossRunReport.model_validate_json(json_data)
            
            print(f"   - Insured: {report.insured_name}")
            print(f"   - Policy: {report.policy_number}")
            
            # Run the compliance rules
            result = evaluate_sop_compliance(report)
            
            print(f"   👉 Underwriting Decision: {result['decision']}")
            
            if result['violations']:
                print("   ❌ Violations Found:")
                for v in result['violations']:
                    print(f"      - {v}")
            
            if result['warnings']:
                print("   ⚠️ Warnings:")
                for w in result['warnings']:
                    print(f"      - {w}")
                    
            if not result['violations'] and not result['warnings']:
                print("   ✅ All carrier guidelines met successfully.")

        except Exception as e:
            print(f"❌ Error evaluating {file_path}: {e}")

    print(f"\n--------------------------------------------------")
    print("🎯 Compliance audit complete!")

if __name__ == "__main__":
    run_compliance_pipeline()