from huggingface_hub import InferenceClient
import logging

logger = logging.getLogger(__name__)

class FarmerCopilotLLM:
    """LLM integration via HuggingFace"""
    
    def __init__(self, hf_token):
        try:
            self.client = InferenceClient(
                model="mistralai/Mistral-7B-Instruct-v0.2",
                token=hf_token
            )
        except Exception as e:
            logger.error(f"LLM initialization failed: {e}")
            self.client = None
    
    def generate_response(self, query, context, history):
        """Generate LLM response"""
        if not self.client:
            return "LLM service unavailable. Please check API key."
        
        try:
            # Build prompt
            system_prompt = """You are an expert agricultural advisor for Indian farmers.
            Provide practical, actionable advice in simple language.
            Explain WHAT, HOW, WHEN, WHERE, and WHY.
            Always prioritize farmer safety."""
            
            # Build message
            if context.get("weather"):
                system_prompt += f"\n\nCurrent weather: {context['weather']['description']}, {context['weather']['temp']}°C"
            
            prompt = f"{system_prompt}\n\nFarmer question: {query}"
            
            # Generate
            response = self.client.text_generation(
                prompt,
                max_new_tokens=300,
                temperature=0.7
            )
            
            return response if response else "Unable to generate response"
            
        except Exception as e:
            logger.error(f"LLM generation error: {e}")
            return f"Error generating response: {str(e)}"
