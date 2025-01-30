# run.py
import uvicorn
from app.config import settings
import sys

def debug_settings():
    """Print current settings for verification"""
    print("\nCurrent settings:")
    for key, value in settings.__dict__.items():
        if not key.startswith('_'):
            print(f"{key}={value}")
    print("\n")

def main():
    try:
        debug_settings()  # Add this to verify settings are loaded correctly
        uvicorn.run(
            "app.main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.RELOAD,
            workers=settings.WORKERS,
            log_level=settings.LOG_LEVEL.lower(),
        )
    except Exception as e:
        print(f"Error starting the server: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()