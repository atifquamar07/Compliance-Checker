# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from app.models.schemas import ComplianceRequest, ComplianceResponse
from app.services.compliance import ComplianceChecker
from app.config import settings
from datetime import datetime

app = FastAPI(
    title="Compliance Checker API",
    description="API for checking webpage content against compliance policies",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/check-compliance", response_model=ComplianceResponse)
async def check_compliance(request: ComplianceRequest):
    """
    Checks webpage content against a specified compliance policy URL.
    
    This endpoint takes two URLs:
    - webpage_url: The webpage to analyze
    - policy_url: The compliance policy to check against
    
    Returns a detailed compliance analysis including any violations found.
    """
    try:
        checker = ComplianceChecker()
        result = await checker.check_compliance(
            webpage_url=str(request.webpage_url),
            policy_url=str(request.policy_url)
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/check-compliance/stream")
async def check_compliance_stream(request: ComplianceRequest):
    """
    Streams compliance check results as they're generated.
    
    This endpoint provides real-time analysis results by:
    1. First extracting rules from the policy URL
    2. Then checking the webpage content against these rules
    3. Streaming violations as they're found
    """
    try:
        checker = ComplianceChecker()
        
        # First fetch both contents
        webpage_content = await checker.web_scraper.fetch_content(str(request.webpage_url))
        policy_content = await checker.web_scraper.fetch_content(str(request.policy_url))
        
        # Start streaming analysis
        return StreamingResponse(
            checker.text_analyzer.analyze_compliance_stream(
                webpage_content=webpage_content,
                policy_content=policy_content
            ),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API availability
    """
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}