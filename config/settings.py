import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings"""
    
    # API Keys
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    DEEPL_API_KEY = os.getenv("DEEPL_API_KEY", "")
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")
    
    # Model Settings
    DISEASE_MODEL_PATH = "models/disease_detection_best.pt"
    FAISS_INDEX_PATH = "data/faiss_index.bin"
    
    # Language Settings
    SUPPORTED_LANGUAGES = ["en", "hi", "mr", "ta", "gu"]
    
    # API Rate Limits
    WEATHER_CACHE_HOURS = 1
    MARKET_CACHE_HOURS = 4
    
    # Application
    DEBUG = os.getenv("DEBUG", "False") == "True"
    MAX_CONVERSATION_HISTORY = 10

settings = Settings()
