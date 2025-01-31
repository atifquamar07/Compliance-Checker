from typing import Dict, List
from datetime import datetime
from app.models.schemas import ComplianceViolation, ComplianceResponse
from app.services.web_scraper import WebScraper
from app.services.text_analyzer import TextAnalyzer
from app.config import settings
from termcolor import colored

class ComplianceChecker:
    def __init__(self):
        self.web_scraper = WebScraper()
        self.text_analyzer = TextAnalyzer()

    async def check_compliance(self, webpage_url: str, policy_url: str) -> ComplianceResponse:
        """
        Checks webpage compliance against a specified policy URL.
        """
        # Fetch content from both URLs
        webpage_content = await self.web_scraper.fetch_content(webpage_url)
        policy_content = await self.web_scraper.fetch_content(policy_url)
        
        # Analyze compliance
        violations = await self.text_analyzer.analyze_compliance(
            webpage_content=webpage_content,
            policy_content=policy_content
        )

        return ComplianceResponse(
            webpage_url=webpage_url,
            policy_url=policy_url,
            violations=violations,
            scan_timestamp=datetime.utcnow().isoformat()
        )