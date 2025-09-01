"""
Base configuration class
"""
from pydantic import BaseSettings

class BaseConfig(BaseSettings):
    """Base configuration settings"""
    
    class Config:
        env_file = ".env"
        case_sensitive = False
