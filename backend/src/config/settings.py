"""
Application settings and configuration
"""

import os
from pathlib import Path
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""


    RAG_DB_PATH: str = "./data/rag_db"
    EMBEDDINGS_MODEL: str = "all-MiniLM-L6-v2"
    LLM_PROVIDER: str = "openai"  # or "ollama"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # LLM Settings
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    OPENAI_MAX_TOKENS: int = 1000
    
    # Hugging Face Settings
    HF_TOKEN: Optional[str] = None
    HF_CACHE_DIR: str = "./data/models/huggingface"
    
    # Embedding Settings
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    EMBEDDING_DIMENSION: int = 384
    
    # Vector Database
    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma_db"
    CHROMA_COLLECTION_NAME: str = "documents"
    
    # Database
    DATABASE_URL: str = "sqlite:///./data/conversations.db"
    
    # ML Experiment Settings
    EXPERIMENTS_DIR: str = "./data/experiments"
    MODELS_DIR: str = "./data/models"
    DATASETS_DIR: str = "./data/datasets"
    VISUALIZATIONS_DIR: str = "./data/visualizations"
    
    # Training Settings
    DEFAULT_BATCH_SIZE: int = 32
    DEFAULT_LEARNING_RATE: float = 0.001
    DEFAULT_EPOCHS: int = 10
    
    # Weights & Biases
    WANDB_PROJECT: str = "ml-ai-backend"
    WANDB_API_KEY: Optional[str] = None
    
    # Device Settings
    DEVICE: str = "auto"  # auto, cpu, cuda, mps
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Ensure directories exist
for directory in [
    settings.EXPERIMENTS_DIR,
    settings.MODELS_DIR,
    settings.DATASETS_DIR,
    settings.VISUALIZATIONS_DIR,
    settings.HF_CACHE_DIR,
    settings.CHROMA_PERSIST_DIRECTORY
]:
    Path(directory).mkdir(parents=True, exist_ok=True)