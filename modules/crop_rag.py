import json
import logging
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

class CropRAGSystem:
    """RAG for crop recommendations"""
    
    def __init__(self):
        self.crops_db = self._load_crops_db()
    
    def _load_crops_db(self):
        """Load crops knowledge base"""
        db = {
            "wheat": {
                "name": "Wheat",
                "season": "Rabi",
                "temp_optimal": (15, 25),
                "rainfall_mm": 400,
                "yield_kg_ha": 4500,
                "price_per_quintal": 2200
            },
            "rice": {
                "name": "Rice",
                "season": "Kharif",
                "temp_optimal": (20, 35),
                "rainfall_mm": 1200,
                "yield_kg_ha": 5500,
                "price_per_quintal": 2500
            },
            "cotton": {
                "name": "Cotton",
                "season": "Kharif",
                "temp_optimal": (20, 30),
                "rainfall_mm": 700,
                "yield_kg_ha": 20,
                "price_per_quintal": 5500
            },
            "soybean": {
                "name": "Soybean",
                "season": "Kharif",
                "temp_optimal": (20, 30),
                "rainfall_mm": 500,
                "yield_kg_ha": 2000,
                "price_per_quintal": 4200
            }
        }
        return db
    
    def get_recommendations(self, soil_params):
        """Get crop recommendations"""
        recommendations = []
        
        for crop_name, crop_data in self.crops_db.items():
            recommendations.append({
                "crop": crop_data["name"],
                "suitability": 85,
                "yield": crop_data["yield_kg_ha"],
                "price": crop_data["price_per_quintal"]
            })
        
        return sorted(recommendations, key=lambda x: x["suitability"], reverse=True)[:5]
