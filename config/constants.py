API_ENDPOINTS = {
    "openweather_current": "https://api.openweathermap.org/data/2.5/weather",
    "openweather_forecast": "https://api.openweathermap.org/data/2.5/forecast",
    "openweather_geo": "https://api.openweathermap.org/geo/1.0/direct",
    "enam": "https://enam.gov.in/api/commodities",
    "agmark": "https://agmarknet.gov.in/SearchCommodityPrice.aspx",
}

# ════════════════════════════════════════════════════════════════════════════
# CROP METADATA
# ════════════════════════════════════════════════════════════════════════════

CROP_DATA = {
    "wheat": {
        "name": "Wheat",
        "scientific_name": "Triticum aestivum",
        "hindi_name": "गेहूँ",
        "season": "Rabi",
        "duration_days": 120,
        "temp_min": 15,
        "temp_max": 25,
        "rainfall_mm": 400,
        "ph_min": 6.5,
        "ph_max": 7.5,
        "yield_kg_ha": 4500,
        "price_per_quintal": 2200,
        "water_requirement_mm": 400,
    },
    "rice": {
        "name": "Rice",
        "scientific_name": "Oryza sativa",
        "hindi_name": "चावल",
        "season": "Kharif",
        "duration_days": 120,
        "temp_min": 20,
        "temp_max": 35,
        "rainfall_mm": 1200,
        "ph_min": 5.5,
        "ph_max": 7.5,
        "yield_kg_ha": 5500,
        "price_per_quintal": 2500,
        "water_requirement_mm": 1200,
    },
    "cotton": {
        "name": "Cotton",
        "scientific_name": "Gossypium herbaceum",
        "hindi_name": "कपास",
        "season": "Kharif",
        "duration_days": 180,
        "temp_min": 20,
        "temp_max": 30,
        "rainfall_mm": 700,
        "ph_min": 6.0,
        "ph_max": 7.5,
        "yield_kg_ha": 20,
        "price_per_quintal": 5500,
        "water_requirement_mm": 700,
    },
    "sugarcane": {
        "name": "Sugarcane",
        "scientific_name": "Saccharum officinarum",
        "hindi_name": "गन्ना",
        "season": "Kharif",
        "duration_days": 300,
        "temp_min": 20,
        "temp_max": 35,
        "rainfall_mm": 1250,
        "ph_min": 6.0,
        "ph_max": 7.5,
        "yield_kg_ha": 60000,
        "price_per_quintal": 295,
        "water_requirement_mm": 1250,
    },
    "soybean": {
        "name": "Soybean",
        "scientific_name": "Glycine max",
        "hindi_name": "सोयाबीन",
        "season": "Kharif",
        "duration_days": 110,
        "temp_min": 20,
        "temp_max": 30,
        "rainfall_mm": 500,
        "ph_min": 6.0,
        "ph_max": 7.5,
        "yield_kg_ha": 2000,
        "price_per_quintal": 4200,
        "water_requirement_mm": 500,
    },
}

# ════════════════════════════════════════════════════════════════════════════
# DISEASE DATA
# ════════════════════════════════════════════════════════════════════════════

DISEASES = {
    "powdery_mildew": {
        "name": "Powdery Mildew",
        "hindi_name": "चूर्णी फफूंद",
        "description": "White powdery growth on leaves",
        "affected_crops": ["wheat", "rice"],
        "symptoms": [
            "White powder on leaves",
            "Yellow leaves",
            "Leaf curling",
            "Stunted growth",
        ],
        "treatment": [
            "Spray Sulfur dust (organic)",
            "Use Carbendazim",
            "Improve air circulation",
            "Reduce humidity",
        ],
        "prevention": [
            "Use resistant varieties",
            "Proper spacing",
            "Avoid excess nitrogen",
            "Timely irrigation",
        ],
    },
    "brown_spot": {
        "name": "Brown Spot",
        "hindi_name": "भूरे धब्बे",
        "description": "Brown spots on leaves and stems",
        "affected_crops": ["rice"],
        "symptoms": [
            "Brown circular spots",
            "Concentric rings",
            "Leaf damage",
            "Reduced yield",
        ],
        "treatment": [
            "Spray Tricyclazole",
            "Use Mancozeb",
            "Remove infected leaves",
        ],
        "prevention": [
            "Clean seeds",
            "Crop rotation",
            "Proper drainage",
            "Balanced fertilization",
        ],
    },
    "leaf_blight": {
        "name": "Leaf Blight",
        "hindi_name": "पत्ती अंगमारी",
        "description": "Large necrotic lesions on leaves",
        "affected_crops": ["rice", "wheat"],
        "symptoms": [
            "Gray-green lesions",
            "Yellow border",
            "Rapid spread",
            "Leaf death",
        ],
        "treatment": [
            "Spray Metalaxyl",
            "Use Copper fungicide",
            "Remove infected plant parts",
        ],
        "prevention": [
            "Use resistant varieties",
            "Avoid overcrowding",
            "Maintain sanitation",
            "Proper air circulation",
        ],
    },
}

# ════════════════════════════════════════════════════════════════════════════
# SOIL TYPES
# ════════════════════════════════════════════════════════════════════════════

SOIL_TYPES = {
    "black_soil": {
        "name": "Black Soil",
        "hindi_name": "काली मिट्टी",
        "characteristics": [
            "Rich in clay",
            "High water retention",
            "Fertile",
            "Good for cotton",
        ],
        "suitable_crops": ["cotton", "sugarcane", "wheat"],
        "ph_range": (6.5, 7.5),
        "drainage": "Poor",
        "water_holding": "High",
    },
    "alluvial": {
        "name": "Alluvial Soil",
        "hindi_name": "दोमट मिट्टी",
        "characteristics": [
            "Deposited by rivers",
            "Fertile",
            "Well-drained",
            "Good structure",
        ],
        "suitable_crops": ["wheat", "rice", "sugarcane"],
        "ph_range": (6.5, 7.5),
        "drainage": "Good",
        "water_holding": "Medium",
    },
    "red_soil": {
        "name": "Red Soil",
        "hindi_name": "लाल मिट्टी",
        "characteristics": [
            "Iron oxide rich",
            "Less fertile",
            "Acidic",
            "Well-drained",
        ],
        "suitable_crops": ["cotton", "peanut", "tobacco"],
        "ph_range": (5.5, 6.5),
        "drainage": "Good",
        "water_holding": "Low",
    },
    "laterite": {
        "name": "Laterite Soil",
        "hindi_name": "लेटराइट मिट्टी",
        "characteristics": [
            "Iron-rich",
            "Hard when dry",
            "Acidic",
            "Low fertility",
        ],
        "suitable_crops": ["tea", "coffee", "coconut"],
        "ph_range": (4.5, 5.5),
        "drainage": "Good",
        "water_holding": "Low",
    },
}

# ════════════════════════════════════════════════════════════════════════════
# FERTILIZER RECOMMENDATIONS
# ════════════════════════════════════════════════════════════════════════════

FERTILIZERS = {
    "nitrogen": {
        "name": "Nitrogen (N)",
        "hindi_name": "नाइट्रोजन",
        "sources": ["Urea", "Ammonium Nitrate", "Manure"],
        "benefits": ["Leaf growth", "Protein formation", "Green color"],
        "deficiency_signs": ["Pale leaves", "Stunted growth", "Poor yield"],
    },
    "phosphorus": {
        "name": "Phosphorus (P)",
        "hindi_name": "फॉस्फोरस",
        "sources": ["Superphosphate", "Rock phosphate", "Bone meal"],
        "benefits": ["Root development", "Flowering", "Energy transfer"],
        "deficiency_signs": ["Purple leaves", "Weak roots", "Poor flowering"],
    },
    "potassium": {
        "name": "Potassium (K)",
        "hindi_name": "पोटेशियम",
        "sources": ["Muriate of potash", "Sulfate of potash", "Wood ash"],
        "benefits": ["Disease resistance", "Fruit quality", "Drought tolerance"],
        "deficiency_signs": ["Leaf edges brown", "Poor fruit quality", "Wilting"],
    },
}

# ════════════════════════════════════════════════════════════════════════════
# GOVERNMENT SCHEMES
# ════════════════════════════════════════════════════════════════════════════

GOVERNMENT_SCHEMES = {
    "pm_kisan": {
        "name": "PM Kisan Samman Nidhi",
        "description": "Income support for farmers",
        "amount": "₹6000/year",
        "eligibility": "All farmers",
        "website": "https://pmkisan.gov.in",
    },
    "pm_fasal_bima": {
        "name": "Pradhan Mantri Fasal Bima Yojana",
        "description": "Crop insurance scheme",
        "amount": "Variable",
        "eligibility": "All farmers",
        "website": "https://pmfby.gov.in",
    },
    "soil_health": {
        "name": "Soil Health Card Scheme",
        "description": "Free soil testing & recommendations",
        "amount": "Free",
        "eligibility": "All farmers",
        "website": "https://soilhealth.dac.gov.in",
    },
}

# ════════════════════════════════════════════════════════════════════════════
# UI/UX CONSTANTS
# ════════════════════════════════════════════════════════════════════════════

UI_STRINGS = {
    "welcome": "🌾 Welcome to Farmer Copilot",
    "chat_placeholder": "Ask about crops, weather, disease prevention...",
    "loading": "🤔 Analyzing your question...",
    "weather": "🌤️ Weather",
    "market": "💰 Market",
    "disease": "🐛 Disease",
    "crop": "🌾 Crop",
}

COLORS = {
    "primary": "#10B981",
    "secondary": "#6B7280",
    "success": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "info": "#3B82F6",
}

# ════════════════════════════════════════════════════════════════════════════
# CACHE SETTINGS
# ════════════════════════════════════════════════════════════════════════════

CACHE = {
    "weather_ttl": 3600,  # 1 hour
    "market_ttl": 14400,  # 4 hours
    "disease_ttl": 86400,  # 24 hours
    "crop_ttl": 604800,  # 1 week
}

# ════════════════════════════════════════════════════════════════════════════
# MODEL CONFIGS
# ════════════════════════════════════════════════════════════════════════════

LLM_CONFIG = {
    "model": "mistralai/Mistral-7B-Instruct-v0.2",
    "max_tokens": 300,
    "temperature": 0.7,
    "top_p": 0.95,
}

DISEASE_DETECTION_CONFIG = {
    "model": "efficientnet-b4",
    "input_size": 224,
    "confidence_threshold": 0.7,
}

# ════════════════════════════════════════════════════════════════════════════
# CONSTANTS CLASS FOR EASY ACCESS
# ════════════════════════════════════════════════════════════════════════════


class CONSTANTS:
    """Constants container for easy access"""

    # API Endpoints
    OPENWEATHER_API = API_ENDPOINTS["openweather_current"]
    ENAM_API = API_ENDPOINTS["enam"]
    AGMARK_API = API_ENDPOINTS["agmark"]

    # Data
    CROP_DATA = CROP_DATA
    DISEASES = DISEASES
    SOIL_TYPES = SOIL_TYPES
    FERTILIZERS = FERTILIZERS
    SCHEMES = GOVERNMENT_SCHEMES

    # UI
    UI_STRINGS = UI_STRINGS
    COLORS = COLORS

    # Configuration
    CACHE_SETTINGS = CACHE
    LLM_CONFIG = LLM_CONFIG
    DISEASE_DETECTION = DISEASE_DETECTION_CONFIG

    @staticmethod
    def get_crop_info(crop_name: str) -> dict:
        """Get crop information by name"""
        crop_key = crop_name.lower().replace(" ", "_")
        return CROP_DATA.get(crop_key, {})

    @staticmethod
    def get_disease_info(disease_name: str) -> dict:
        """Get disease information by name"""
        disease_key = disease_name.lower().replace(" ", "_")
        return DISEASES.get(disease_key, {})

    @staticmethod
    def get_soil_info(soil_type: str) -> dict:
        """Get soil type information"""
        soil_key = soil_type.lower().replace(" ", "_")
        return SOIL_TYPES.get(soil_key, {})

    @staticmethod
    def get_suitable_crops(soil_type: str) -> list:
        """Get crops suitable for soil type"""
        soil_key = soil_type.lower().replace(" ", "_")
        soil_info = SOIL_TYPES.get(soil_key, {})
        return soil_info.get("suitable_crops", [])
