import deepl
import langdetect
import logging

logger = logging.getLogger(__name__)

class MultilingualProcessor:
    """Handle multilingual translation"""
    
    SUPPORTED_LANGUAGES = {
        "en": "English",
        "hi": "Hindi",
        "mr": "Marathi",
        "gu": "Gujarati",
        "ta": "Tamil"
    }
    
    def __init__(self, deepl_api_key):
        try:
            self.translator = deepl.Translator(deepl_api_key)
        except Exception as e:
            logger.error(f"DeepL initialization failed: {e}")
            self.translator = None
    
    def detect_language(self, text):
        """Detect language"""
        try:
            lang_code = langdetect.detect(text)
            return self.SUPPORTED_LANGUAGES.get(lang_code, "English")
        except:
            return "English"
    
    def translate_to_english(self, text, source_language):
        """Translate to English"""
        if source_language == "English" or not self.translator:
            return text
        
        lang_map = {
            "Hindi": "HI",
            "Marathi": "EN",
            "Tamil": "TA",
            "Gujarati": "EN"
        }
        
        try:
            source_code = lang_map.get(source_language, "EN")
            result = self.translator.translate_text(text, source_lang=source_code, target_lang="EN")
            return result.text
        except Exception as e:
            logger.warning(f"Translation failed: {e}")
            return text
    
    def translate_response(self, text, target_language):
        """Translate response to target language"""
        if target_language == "English" or not self.translator:
            return text
        
        lang_map = {
            "Hindi": "HI",
            "Marathi": "EN",
            "Tamil": "TA",
            "Gujarati": "EN"
        }
        
        try:
            target_code = lang_map.get(target_language, "EN")
            result = self.translator.translate_text(text, source_lang="EN", target_lang=target_code)
            return result.text
        except Exception as e:
            logger.warning(f"Translation failed: {e}")
            return text
