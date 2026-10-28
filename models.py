from pydantic import BaseModel, Field
from typing import List

class ClaimItem(BaseModel):
    claim_number: str = Field(description="Unique claim identification code, e.g., CL-2024-01")
    date_of_loss: str = Field(description="Date when the incident occurred")
    status: str = Field(description="Claim status such as Open or Closed")
    cause_description: str = Field(description="Brief narrative of the cause of loss")
    paid_loss: str = Field(description="Paid loss amount")
    reserves: str = Field(description="Current reserve amount")
    total_incurred: str = Field(description="Total incurred cost")

class LossRunReport(BaseModel):
    insured_name: str = Field(description="Name of the named insured")
    policy_number: str = Field(description="Insurance policy number")
    valuation_date: str = Field(description="Report valuation date")
    claims: List[ClaimItem] = Field(description="List of individual claim records")