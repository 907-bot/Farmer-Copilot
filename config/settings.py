import os
from dotenv import load_dotenv
import streamlit as st
import logging

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


class Settings:
    """
    Application settings and configuration.
    Automatically handles both local (.env) and HF Spaces (secrets) environments.
    """

    def __init__(self):
        """Initialize settings from environment or Streamlit secrets"""
        self._load_api_keys()
        self._load_app_config()
        self._load_model_paths()
        self._load_feature_flags()

    def _load_api_keys(self):
        """Load API keys from Streamlit secrets or .env file"""
        try:
            # Try Streamlit secrets first (HF Spaces)
            self.OPENWEATHER_API_KEY = st.secrets.get("OPENWEATHER_API_KEY", "")
            self.DEEPL_API_KEY = st.secrets.get("DEEPL_API_KEY", "")
            self.HUGGINGFACE_TOKEN = st.secrets.get("HUGGINGFACE_TOKEN", "")
        except:
            # Fallback to .env file (local development)
            self.OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
            self.DEEPL_API_KEY = os.getenv("DEEPL_API_KEY", "")
            self.HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")

        # Validate that at least LLM token is present
        if not self.HUGGINGFACE_TOKEN:
            logger.warning("⚠️ HUGGINGFACE_TOKEN not found in secrets or .env")

    def _load_app_config(self):
        """Load application configuration"""
        # Supported Languages
        self.SUPPORTED_LANGUAGES = {
            "en": "English",
            "hi": "Hindi",
            "mr": "Marathi",
            "gu": "Gujarati",
            "ta": "Tamil",
            "kn": "Kannada",
            "te": "Telugu",
            "bn": "Bengali",
        }

        # Crops Database
        self.SUPPORTED_CROPS = [
            "Wheat",
            "Rice",
            "Cotton",
            "Sugarcane",
            "Soybean",
            "Corn",
            "Pulses",
            "Vegetables",
            "Fruits",
            "Other",
        ]

        # Soil Types
        self.SOIL_TYPES = [
            "Black Soil",
            "Alluvial",
            "Red Soil",
            "Laterite",
            "Chalky",
            "Sandy",
            "Clay",
            "Loamy",
        ]

        # Seasons
        self.SEASONS = ["Kharif", "Rabi", "Summer", "Winter"]

        # Application name and version
        self.APP_NAME = "🌾 Farmer Copilot"
        self.APP_VERSION = "1.0.0"
        self.APP_DESCRIPTION = "AI-powered agricultural assistant for Indian farmers"

    def _load_model_paths(self):
        """Load model and data file paths"""
        # Base directories
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.DATA_DIR = os.path.join(self.BASE_DIR, "data")
        self.MODELS_DIR = os.path.join(self.BASE_DIR, "models")

        # Create directories if they don't exist
        os.makedirs(self.DATA_DIR, exist_ok=True)
        os.makedirs(self.MODELS_DIR, exist_ok=True)

        # Model and data file paths
        self.DISEASE_MODEL_PATH = os.path.join(
            self.MODELS_DIR, "disease_detection_best.pt"
        )
        self.FAISS_INDEX_PATH = os.path.join(self.DATA_DIR, "faiss_index.bin")
        self.CROPS_KB_PATH = os.path.join(self.DATA_DIR, "crops_kb.json")
        self.DISEASES_DB_PATH = os.path.join(self.DATA_DIR, "diseases.json")

    def _load_feature_flags(self):
        """Load feature flags and application settings"""
        # Debug mode (only affects local, not HF)
        self.DEBUG = os.getenv("DEBUG", "False").lower() == "true"

        # API Rate Limits & Caching
        self.WEATHER_CACHE_HOURS = 1
        self.MARKET_CACHE_HOURS = 4
        self.DISEASE_DETECTION_CACHE_HOURS = 24

        # Chat Settings
        self.MAX_CONVERSATION_HISTORY = 10
        self.MAX_INPUT_LENGTH = 500
        self.LLM_MAX_TOKENS = 300
        self.LLM_TEMPERATURE = 0.7

        # Streamlit Settings
        self.STREAMLIT_PAGE_LAYOUT = "wide"
        self.STREAMLIT_INITIAL_SIDEBAR_STATE = "expanded"

        # Feature Flags
        self.ENABLE_WEATHER = True
        self.ENABLE_MARKET_PRICES = True
        self.ENABLE_DISEASE_DETECTION = True
        self.ENABLE_CROP_RECOMMENDATIONS = True
        self.ENABLE_MULTILINGUAL = True

        # Default Location (if not provided)
        self.DEFAULT_LOCATION = "Nashik, Maharashtra"
        self.DEFAULT_CROP = "Wheat"
        self.DEFAULT_LANGUAGE = "English"

    def validate(self):
        """Validate critical settings"""
        errors = []

        if not self.HUGGINGFACE_TOKEN:
            errors.append("HUGGINGFACE_TOKEN is required")

        if errors:
            logger.error("Configuration validation failed:")
            for error in errors:
                logger.error(f"  - {error}")
            return False

        return True

    def log_config(self):
        """Log configuration (without exposing secrets)"""
        logger.info("=" * 60)
        logger.info("Application Configuration Loaded")
        logger.info("=" * 60)
        logger.info(f"App: {self.APP_NAME} v{self.APP_VERSION}")
        logger.info(f"Debug Mode: {self.DEBUG}")
        logger.info(f"Supported Languages: {len(self.SUPPORTED_LANGUAGES)}")
        logger.info(f"Supported Crops: {len(self.SUPPORTED_CROPS)}")
        logger.info(f"API Keys Available:")
        logger.info(f"  - DeepL: {'✓' if self.DEEPL_API_KEY else '✗'}")
        logger.info(f"  - OpenWeather: {'✓' if self.OPENWEATHER_API_KEY else '✗'}")
        logger.info(f"  - HuggingFace: {'✓' if self.HUGGINGFACE_TOKEN else '✗'}")
        logger.info(f"Features Enabled:")
        logger.info(f"  - Weather: {self.ENABLE_WEATHER}")
        logger.info(f"  - Market Prices: {self.ENABLE_MARKET_PRICES}")
        logger.info(f"  - Disease Detection: {self.ENABLE_DISEASE_DETECTION}")
        logger.info(f"  - Multilingual: {self.ENABLE_MULTILINGUAL}")
        logger.info("=" * 60)

    def get_api_key(self, key_name: str) -> str:
        """Get API key safely"""
        key = getattr(self, f"{key_name.upper()}_API_KEY", None) or getattr(
            self, f"{key_name.upper()}_TOKEN", None
        )
        if not key:
            logger.warning(f"API key '{key_name}' not configured")
        return key or ""

    def to_dict(self):
        """Export configuration as dictionary (excluding secrets)"""
        return {
            "app_name": self.APP_NAME,
            "app_version": self.APP_VERSION,
            "debug": self.DEBUG,
            "languages": self.SUPPORTED_LANGUAGES,
            "crops": self.SUPPORTED_CROPS,
            "soil_types": self.SOIL_TYPES,
            "api_keys_available": {
                "deepl": bool(self.DEEPL_API_KEY),
                "openweather": bool(self.OPENWEATHER_API_KEY),
                "huggingface": bool(self.HUGGINGFACE_TOKEN),
            },
            "features": {
                "weather": self.ENABLE_WEATHER,
                "market_prices": self.ENABLE_MARKET_PRICES,
                "disease_detection": self.ENABLE_DISEASE_DETECTION,
                "crop_recommendations": self.ENABLE_CROP_RECOMMENDATIONS,
                "multilingual": self.ENABLE_MULTILINGUAL,
            },
        }


# Global settings instance
settings = Settings()

# Validate on import
if not settings.validate():
    logger.error("Configuration validation failed. Some features may not work.")
