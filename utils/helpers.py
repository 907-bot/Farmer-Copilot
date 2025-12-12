import requests
import logging
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import json
import re
import streamlit as st
from config import settings, CONSTANTS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ════════════════════════════════════════════════════════════════════════════
# WEATHER UTILITIES
# ════════════════════════════════════════════════════════════════════════════


def get_location_coordinates(location: str) -> Optional[Tuple[float, float]]:
    """
    Get latitude and longitude from location name using OpenWeather Geo API.
    
    Args:
        location (str): Location name (e.g., "Nashik, Maharashtra")
    
    Returns:
        Tuple[float, float]: (latitude, longitude) or None if error
    """
    if not location or not settings.OPENWEATHER_API_KEY:
        logger.warning("Location or API key missing")
        return None
    
    try:
        geo_url = "https://api.openweathermap.org/geo/1.0/direct"
        params = {
            "q": location,
            "limit": 1,
            "appid": settings.OPENWEATHER_API_KEY
        }
        
        response = requests.get(geo_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data:
            return (data[0]['lat'], data[0]['lon'])
        return None
    
    except Exception as e:
        logger.error(f"Error getting coordinates: {str(e)}")
        return None


def get_weather_data(location: str) -> Optional[Dict[str, Any]]:
    """
    Get current weather data for a location.
    
    Args:
        location (str): Location name
    
    Returns:
        Dict with weather data or None if error
        Structure: {
            'temperature': float,
            'humidity': int,
            'pressure': int,
            'wind_speed': float,
            'description': str,
            'location': str,
            'country': str,
            'timestamp': str
        }
    """
    if not settings.OPENWEATHER_API_KEY:
        logger.warning("OpenWeather API key not configured")
        return None
    
    try:
        # Get coordinates first
        coords = get_location_coordinates(location)
        if not coords:
            return None
        
        lat, lon = coords
        
        # Get weather data
        weather_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "lat": lat,
            "lon": lon,
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric"
        }
        
        response = requests.get(weather_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        weather_info = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'],
            'location': data['name'],
            'country': data['sys']['country'],
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f"Weather data retrieved for {location}")
        return weather_info
    
    except Exception as e:
        logger.error(f"Error getting weather data: {str(e)}")
        return None


def format_weather_response(weather_data: Dict[str, Any]) -> str:
    """
    Format weather data into a readable response.
    
    Args:
        weather_data (Dict): Weather data from get_weather_data()
    
    Returns:
        str: Formatted weather response
    """
    if not weather_data:
        return "Unable to fetch weather data. Please try again."
    
    response = f"""
🌤️ **Weather in {weather_data['location']}, {weather_data['country']}**

📊 Current Conditions:
- Temperature: {weather_data['temperature']:.1f}°C
- Humidity: {weather_data['humidity']}%
- Pressure: {weather_data['pressure']} hPa
- Wind Speed: {weather_data['wind_speed']} m/s
- Condition: {weather_data['description'].capitalize()}

⏰ Updated at: {weather_data['timestamp']}

💡 **Agricultural Tips:**
- For Kharif crops: Monitor humidity for disease prevention
- For Rabi crops: Current temperature is suitable for most crops
- For irrigation: Check humidity before watering
"""
    return response.strip()


# ════════════════════════════════════════════════════════════════════════════
# MARKET PRICE UTILITIES
# ════════════════════════════════════════════════════════════════════════════


def get_market_prices(crop: str, location: str = "Maharashtra") -> Optional[Dict[str, Any]]:
    """
    Get market prices for a crop.
    (Placeholder - can be connected to real e-NAM or AGMARK API)
    
    Args:
        crop (str): Crop name
        location (str): Location/state
    
    Returns:
        Dict with price data or mock data
    """
    try:
        # For now, return mock data based on CONSTANTS
        crop_key = crop.lower().replace(" ", "_")
        crop_info = CONSTANTS.get_crop_info(crop_key)
        
        if not crop_info:
            return None
        
        mock_prices = {
            'crop': crop,
            'location': location,
            'price_per_quintal': crop_info.get('price_per_quintal', 2000),
            'price_per_kg': crop_info.get('price_per_quintal', 2000) / 100,
            'market': 'e-NAM/AGMARK',
            'last_updated': datetime.now().isoformat(),
            'trend': 'stable',
            'min_price': crop_info.get('price_per_quintal', 2000) * 0.9,
            'max_price': crop_info.get('price_per_quintal', 2000) * 1.1,
            'avg_price': crop_info.get('price_per_quintal', 2000)
        }
        
        logger.info(f"Market prices retrieved for {crop}")
        return mock_prices
    
    except Exception as e:
        logger.error(f"Error getting market prices: {str(e)}")
        return None


def format_price_response(price_data: Dict[str, Any]) -> str:
    """
    Format market price data into readable response.
    
    Args:
        price_data (Dict): Price data from get_market_prices()
    
    Returns:
        str: Formatted price response
    """
    if not price_data:
        return "Unable to fetch market prices. Please try again."
    
    response = f"""
💰 **Market Prices for {price_data['crop']}** in {price_data['location']}

📊 Price Information:
- Current Price: ₹{price_data['price_per_quintal']:.0f}/quintal
- Price per Kg: ₹{price_data['price_per_kg']:.2f}
- Minimum Price: ₹{price_data['min_price']:.0f}/quintal
- Maximum Price: ₹{price_data['max_price']:.0f}/quintal
- Average Price: ₹{price_data['avg_price']:.0f}/quintal
- Market Trend: {price_data['trend'].capitalize()}

📍 Source: {price_data['market']}
⏰ Last Updated: {price_data['last_updated']}

💡 **Tips for Farmers:**
- Compare prices across different mandis
- Time your harvest when prices are favorable
- Consider storage if prices are low
- Monitor market trends for better planning
"""
    return response.strip()


# ════════════════════════════════════════════════════════════════════════════
# TEXT UTILITIES
# ════════════════════════════════════════════════════════════════════════════


def detect_language(text: str) -> str:
    """
    Detect language of input text.
    
    Args:
        text (str): Input text
    
    Returns:
        str: Language code (en, hi, mr, etc.)
    """
    try:
        # Simple language detection based on unicode ranges
        hindi_pattern = re.compile('[\u0900-\u097F]')
        marathi_pattern = re.compile('[\u0900-\u097F]')  # Same as Hindi
        gujarati_pattern = re.compile('[\u0A80-\u0AFF]')
        tamil_pattern = re.compile('[\u0B80-\u0BFF]')
        
        if hindi_pattern.search(text):
            return 'hi'
        elif gujarati_pattern.search(text):
            return 'gu'
        elif tamil_pattern.search(text):
            return 'ta'
        else:
            return 'en'
    
    except Exception as e:
        logger.error(f"Error detecting language: {str(e)}")
        return 'en'


def translate_text(text: str, target_language: str) -> Optional[str]:
    """
    Translate text using DeepL API.
    
    Args:
        text (str): Text to translate
        target_language (str): Target language code
    
    Returns:
        str: Translated text or original if error
    """
    if not settings.DEEPL_API_KEY or target_language == 'en':
        return text
    
    try:
        # Map language codes to DeepL language codes
        lang_map = {
            'hi': 'HI',
            'mr': 'HI',  # Marathi uses Hindi model
            'gu': 'gu',
            'ta': 'TA',
            'kn': 'KN',
            'te': 'TE',
            'bn': 'BN',
        }
        
        target_lang = lang_map.get(target_language, 'EN')
        
        url = "https://api-free.deepl.com/v1/translate"
        params = {
            "auth_key": settings.DEEPL_API_KEY,
            "text": text,
            "target_lang": target_lang
        }
        
        response = requests.post(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data['translations']:
            return data['translations'][0]['text']
        return text
    
    except Exception as e:
        logger.error(f"Error translating text: {str(e)}")
        return text


def clean_input(text: str) -> str:
    """
    Clean and normalize user input.
    
    Args:
        text (str): Raw user input
    
    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove special characters but keep common punctuation
    text = re.sub(r'[^\w\s\.\,\?\!\-]', '', text)
    
    # Limit length
    text = truncate_text(text, settings.MAX_INPUT_LENGTH)
    
    return text.strip()


def truncate_text(text: str, max_length: int = 500) -> str:
    """
    Truncate text to maximum length.
    
    Args:
        text (str): Text to truncate
        max_length (int): Maximum length
    
    Returns:
        str: Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."


# ════════════════════════════════════════════════════════════════════════════
# AI UTILITIES
# ════════════════════════════════════════════════════════════════════════════


def generate_crop_recommendation(
    soil_type: str,
    season: str,
    rainfall: int,
    temperature: float
) -> str:
    """
    Generate crop recommendation based on conditions.
    
    Args:
        soil_type (str): Soil type
        season (str): Season
        rainfall (int): Annual rainfall in mm
        temperature (float): Average temperature
    
    Returns:
        str: Crop recommendation
    """
    recommendations = []
    
    for crop_key, crop_data in CONSTANTS.CROP_DATA.items():
        score = 0
        
        # Check soil suitability
        suitable_soils = CONSTANTS.get_suitable_crops(soil_type)
        if crop_key in suitable_soils:
            score += 30
        
        # Check season
        if crop_data['season'].lower() == season.lower():
            score += 20
        
        # Check rainfall
        if abs(crop_data['rainfall_mm'] - rainfall) < 300:
            score += 20
        
        # Check temperature
        if crop_data['temp_min'] <= temperature <= crop_data['temp_max']:
            score += 30
        
        if score > 0:
            recommendations.append((crop_data['name'], score))
    
    # Sort by score
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    if recommendations:
        top_crops = [crop[0] for crop in recommendations[:3]]
        return f"🌾 **Recommended Crops:** {', '.join(top_crops)}\n\nBased on your soil type, season, and climate conditions."
    
    return "🌾 **Unable to recommend crops.** Please provide more detailed information."


def get_disease_treatment(disease: str) -> Optional[str]:
    """
    Get treatment information for a disease.
    
    Args:
        disease (str): Disease name
    
    Returns:
        str: Disease treatment information
    """
    disease_key = disease.lower().replace(" ", "_")
    disease_info = CONSTANTS.get_disease_info(disease_key)
    
    if not disease_info:
        return f"No information found for disease: {disease}"
    
    treatment_text = f"""
🐛 **Disease:** {disease_info['name']}
📖 **Description:** {disease_info['description']}

🔍 **Symptoms:**
{chr(10).join([f'• {symptom}' for symptom in disease_info.get('symptoms', [])])}

💊 **Treatment Methods:**
{chr(10).join([f'• {method}' for method in disease_info.get('treatment', [])])}

🛡️ **Prevention Strategies:**
{chr(10).join([f'• {prev}' for prev in disease_info.get('prevention', [])])}
"""
    return treatment_text.strip()


def format_llm_response(response_text: str, max_tokens: int = 300) -> str:
    """
    Format LLM response for better display.
    
    Args:
        response_text (str): Raw LLM response
        max_tokens (int): Maximum tokens to keep
    
    Returns:
        str: Formatted response
    """
    # Truncate if too long
    response_text = truncate_text(response_text, max_tokens)
    
    # Clean up formatting
    response_text = response_text.strip()
    
    # Add markdown formatting if missing
    if not response_text.startswith('#'):
        response_text = f"💬 {response_text}"
    
    return response_text


# ════════════════════════════════════════════════════════════════════════════
# CACHE UTILITIES
# ════════════════════════════════════════════════════════════════════════════


def get_cache_key(
    function_name: str,
    *args,
    **kwargs
) -> str:
    """
    Generate cache key for a function call.
    
    Args:
        function_name (str): Name of function
        *args: Function arguments
        **kwargs: Function keyword arguments
    
    Returns:
        str: Cache key
    """
    cache_data = f"{function_name}:{str(args)}:{str(kwargs)}"
    return hashlib.md5(cache_data.encode()).hexdigest()


def is_cache_valid(
    cache_timestamp: Optional[float],
    ttl_seconds: int
) -> bool:
    """
    Check if cached data is still valid.
    
    Args:
        cache_timestamp (float): When data was cached
        ttl_seconds (int): Time to live in seconds
    
    Returns:
        bool: True if cache is still valid
    """
    if cache_timestamp is None:
        return False
    
    return (time.time() - cache_timestamp) < ttl_seconds


# ════════════════════════════════════════════════════════════════════════════
# ERROR HANDLING UTILITIES
# ════════════════════════════════════════════════════════════════════════════


def handle_api_error(error: Exception, context: str = "") -> str:
    """
    Handle API errors gracefully.
    
    Args:
        error (Exception): The error that occurred
        context (str): Context where error occurred
    
    Returns:
        str: User-friendly error message
    """
    error_str = str(error).lower()
    
    if "timeout" in error_str:
        return f"⏱️ Request timed out. {context} Please try again."
    elif "connection" in error_str:
        return f"🌐 Connection error. {context} Check your internet connection."
    elif "401" in error_str or "unauthorized" in error_str:
        return f"🔐 Authentication failed. {context} Please check API credentials."
    elif "404" in error_str or "not found" in error_str:
        return f"🔍 Resource not found. {context} Please verify your input."
    elif "rate limit" in error_str:
        return f"⚠️ API rate limit exceeded. {context} Please wait a moment and try again."
    else:
        return f"❌ An error occurred: {error}. {context} Please try again later."


def log_error(
    error: Exception,
    function_name: str,
    user_input: Optional[str] = None
) -> None:
    """
    Log errors with context information.
    
    Args:
        error (Exception): The error
        function_name (str): Where error occurred
        user_input (str): User input that caused error
    """
    error_msg = f"""
ERROR in {function_name}:
  Error Type: {type(error).__name__}
  Error Message: {str(error)}
  User Input: {user_input}
  Timestamp: {datetime.now().isoformat()}
"""
    logger.error(error_msg)


# ════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════


def format_timestamp(timestamp: Optional[str] = None) -> str:
    """
    Format timestamp for display.
    
    Args:
        timestamp (str): ISO format timestamp
    
    Returns:
        str: Formatted timestamp
    """
    if not timestamp:
        timestamp = datetime.now().isoformat()
    
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return timestamp


def get_season_from_month(month: int) -> str:
    """
    Get season from month number.
    
    Args:
        month (int): Month (1-12)
    
    Returns:
        str: Season name
    """
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Summer"
    elif month in [6, 7, 8, 9]:
        return "Monsoon"
    else:  # 10, 11
        return "Post-Monsoon"


def get_health_status(
    temperature: float,
    humidity: int,
    rainfall: int
) -> Tuple[str, str]:
    """
    Determine crop health status based on conditions.
    
    Args:
        temperature (float): Current temperature
        humidity (int): Current humidity
        rainfall (int): Recent rainfall
    
    Returns:
        Tuple[str, str]: (status, emoji)
    """
    issues = []
    
    if temperature > 40:
        issues.append("High temperature - water crops regularly")
    elif temperature < 10:
        issues.append("Low temperature - monitor for frost damage")
    
    if humidity > 80:
        issues.append("High humidity - watch for fungal diseases")
    elif humidity < 30:
        issues.append("Low humidity - increase irrigation")
    
    if rainfall < 200:
        issues.append("Low rainfall - supplemental irrigation needed")
    elif rainfall > 1000:
        issues.append("High rainfall - ensure good drainage")
    
    if issues:
        return ("\n".join([f"⚠️ {issue}" for issue in issues]), "⚠️")
    else:
        return ("✅ Conditions are favorable for crop growth", "✅")
