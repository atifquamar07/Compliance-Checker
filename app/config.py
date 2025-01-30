# app/config.py
from pydantic_settings import BaseSettings
from typing import List, Dict

class Settings(BaseSettings):
    # Server Settings
    PORT: int = 8050
    HOST: str = "0.0.0.0"
    WORKERS: int = 4
    RELOAD: bool = True

    # API Settings
    GROQ_API_KEY: str

    # Application Settings
    LOG_LEVEL: str = "INFO"
    MAX_CONCURRENT_REQUESTS: int = 50

    # Web Scraping Settings
    REQUEST_TIMEOUT: int = 30
    MAX_CONTENT_SIZE: int = 10
    USER_AGENT: str = "Compliance-Checker-Bot/1.0"

    # Compliance Settings
    MIN_COMPLIANCE_SCORE: int = 80
    MAX_VIOLATIONS: int = 10
    DETAILED_REPORTING: bool = True

    # Cache Settings
    ENABLE_CACHE: bool = True
    CACHE_TTL: int = 86400

    # Security Settings
    ENABLE_RATE_LIMIT: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60

    # Development Settings
    DEBUG: bool = True
    ENABLE_CORS: bool = True
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:8080"
    
    COMPLIANCE_RULES: Dict = {
        "treasury_terms": [
            "banking services",
            "deposit account",
            "financial institution",
            "FDIC"
        ],
        "prohibited_phrases": [
            "bank account",
            "checking account",
            "savings account"
        ],
        "disclaimer_required": True,
        "disclaimer_text": "Banking services provided by bank partners"
    }

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert the comma-separated CORS_ORIGINS string to a list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()