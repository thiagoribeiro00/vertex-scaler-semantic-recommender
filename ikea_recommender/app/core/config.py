import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "IKEA-SmartSuggest"
    API_V1_STR: str = "/api/v1"
    
    # GCP Config
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "your-project-id")
    GCP_LOCATION: str = os.getenv("GCP_LOCATION", "us-central1")
    VERTEX_AI_INDEX_ID: str = os.getenv("VERTEX_AI_INDEX_ID", "your-index-id")
    
    # Redis Config
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    
    # Data Paths
    BASE_DATA_PATH: str = os.getenv("BASE_DATA_PATH", "data/")

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
