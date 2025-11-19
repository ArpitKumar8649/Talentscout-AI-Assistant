"""Application settings and configuration management"""
import os
from pydantic_settings import BaseSettings
from typing import Optional

def get_streamlit_secrets():
    """Get secrets from Streamlit Cloud or return None for local development"""
    try:
        import streamlit as st
        return st.secrets
    except:
        return None

class Settings(BaseSettings):
    """Application settings loaded from environment variables or Streamlit secrets"""
    
    # Letta Configuration
    letta_api_key: str = "placeholder"
    letta_agent_id: str = "placeholder"
    letta_project_id: str = "placeholder"
    letta_base_url: str = "https://api.letta.com"
    
    # MongoDB Configuration (Optional)
    mongo_url: str = "mongodb://localhost:27017"
    db_name: str = "talentscout_db"
    
    # Application Settings
    app_title: str = "TalentScout AI Hiring Assistant"
    app_icon: str = "💼"
    debug_mode: bool = False
    
    class Config:
        env_file = ".env.streamlit"
        case_sensitive = False
        extra = "allow"
    
    def __init__(self, **kwargs):
        """Initialize settings, prioritizing Streamlit secrets over env vars"""
        super().__init__(**kwargs)
        
        # Override with Streamlit secrets if available (for cloud deployment)
        secrets = get_streamlit_secrets()
        if secrets:
            self.letta_api_key = secrets.get("LETTA_API_KEY", self.letta_api_key)
            self.letta_agent_id = secrets.get("LETTA_AGENT_ID", self.letta_agent_id)
            self.letta_project_id = secrets.get("LETTA_PROJECT_ID", self.letta_project_id)
            self.letta_base_url = secrets.get("LETTA_BASE_URL", self.letta_base_url)
            self.mongo_url = secrets.get("MONGO_URL", self.mongo_url)
            self.db_name = secrets.get("DB_NAME", self.db_name)
            self.app_title = secrets.get("APP_TITLE", self.app_title)
            self.app_icon = secrets.get("APP_ICON", self.app_icon)
            self.debug_mode = secrets.get("DEBUG_MODE", self.debug_mode)

# Global settings instance
settings = Settings()
