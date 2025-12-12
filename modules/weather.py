import requests
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class WeatherAPI:
    """OpenWeather API integration"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_weather(self, location):
        """Get current weather"""
        try:
            # Geocode
            geo_url = f"{self.base_url}/weather"
            params = {
                "q": location,
                "appid": self.api_key,
                "units": "metric"
            }
            
            response = requests.get(geo_url, params=params, timeout=5)
            data = response.json()
            
            if response.status_code == 200:
                return {
                    "location": location,
                    "temp": data["main"]["temp"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"]["description"],
                    "wind_speed": data["wind"]["speed"],
                    "pressure": data["main"]["pressure"]
                }
            else:
                return {
                    "error": "Location not found",
                    "temp": 25,
                    "humidity": 60
                }
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            return {
                "error": str(e),
                "temp": 25,
                "humidity": 60
            }
