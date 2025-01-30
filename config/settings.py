import logging
import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file
load_dotenv()

# Pydantic settings for typed env variables
class Settings(BaseSettings):
    GITHUB_API_BASE: str
    CORS_ORIGIN: str = "*"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

# Global settings instance
settings = Settings()

def setup_cors(app):
    """Configures CORS to allow requests from specified origins."""
    origins = [settings.CORS_ORIGIN] if settings.CORS_ORIGIN != "*" else ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def setup_logging():
    """Configures logging settings."""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    return logger
