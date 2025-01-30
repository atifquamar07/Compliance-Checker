# app/models/schemas.py
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Optional

class ComplianceRequest(BaseModel):
    webpage_url: HttpUrl
    policy_url: HttpUrl

class ComplianceViolation(BaseModel):
    type: str
    description: str
    context: str
    severity: str
    suggestion: str

class ComplianceResponse(BaseModel):
    webpage_url: str
    policy_url: str
    violations: List[ComplianceViolation]
    scan_timestamp: str