from pydantic import BaseModel, Field
from typing import List,Literal

class Claim(BaseModel): 
    id: int = Field(..., description="number run from 1 to total number of claims extracted")
    claim: str = Field(..., description="The exact statement representing a factual claim.")
    source: str = Field(..., description="Supporting URL or empty string")
    support: Literal["yes", "no", "unknown"] = Field(..., description="Whether the claim is supported.")
class ExtractFactualClaimsOutput(BaseModel):
    claims: List[Claim] = Field(
        ..., 
        description="List of extracted factual claims"
    )

class VerificationItem(BaseModel):
    id: int = Field(...,description="The identifier of the claim (must match the input claim id).")
    result: Literal["yes", "no", "unknown"] = Field(...,description="Verification outcome for the claim: 'yes' if supported, 'no' if not supported, 'unknown' if verification is impossible or reference unavailable.")
class ClaimVerification(BaseModel):
    verifications: List[VerificationItem] = Field(...,description="An array of verification results, one per claim.")

