"""Configuration management"""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Database Configuration
    database_url: str = "postgresql://user:password@localhost:5432/visa_disputes"
    
    # ChromaDB Configuration
    chromadb_host: str = "localhost"
    chromadb_port: int = 8000
    
    # Enrichment Service
    enrichment_api_url: str = "http://localhost:8001/api/v1"
    
    # Gmail API
    gmail_api_credentials: Optional[str] = None
    
    # SMTP Configuration for email sending
    smtp_email: str = ""
    smtp_password: str = ""
    
    # LLM Configuration
    llm_api_key: str = "not-needed-for-ollama"
    llm_model: str = "llama3.2"
    llm_provider: str = "ollama"  # "openai", "google", or "ollama"
    
    # Application Configuration
    log_level: str = "INFO"
    max_retry_attempts: int = 3
    confidence_threshold: float = 0.85
    similarity_threshold: float = 0.7
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Set API key based on provider
if settings.llm_provider == "google":
    os.environ["GOOGLE_API_KEY"] = settings.llm_api_key
elif settings.llm_provider == "openai":
    os.environ["OPENAI_API_KEY"] = settings.llm_api_key
# Ollama doesn't need API keys
