import streamlit as st
import sys
from pathlib import Path
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="🌾 Farmer Copilot",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# CSS Styling
st.markdown("""
<style>
    .main { padding: 2rem; }
    .header { text-align: center; margin-bottom: 2rem; }
    .chat-box { 
        border: 1px solid #ddd; 
        padding: 1rem; 
        border-radius: 0.5rem;
        margin: 1rem 0;
        background-color: #f9fafb;
    }
    .farmer-input { 
        border: 2px solid #10B981; 
        padding: 0.5rem; 
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "user_location" not in st.session_state:
    st.session_state.user_location = None

# Get API Keys
try:
    DEEPL_KEY = st.secrets.get("DEEPL_API_KEY", os.getenv("DEEPL_API_KEY"))
    OPENWEATHER_KEY = st.secrets.get("OPENWEATHER_API_KEY", os.getenv("OPENWEATHER_API_KEY"))
    HF_TOKEN = st.secrets.get("HUGGINGFACE_TOKEN", os.getenv("HUGGINGFACE_TOKEN"))
except:
    DEEPL_KEY = os.getenv("DEEPL_API_KEY")
    OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")
    HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Import modules
try:
    from modules.weather import WeatherAPI
    from modules.market import MarketAPI
    from modules.crop_rag import CropRAGSystem
    from modules.disease_detection import DiseaseDetector
    from modules.llm_engine import FarmerCopilotLLM
    from nlp.translator import MultilingualProcessor
except ImportError as e:
    st.error(f"Error importing modules: {e}")
    st.stop()

# Initialize components with caching
@st.cache_resource
def initialize_components():
    """Initialize all components"""
    try:
        weather_api = WeatherAPI(OPENWEATHER_KEY)
        market_api = MarketAPI()
        crop_rag = CropRAGSystem()
        disease_detector = DiseaseDetector()
        llm = FarmerCopilotLLM(HF_TOKEN)
        translator = MultilingualProcessor(DEEPL_KEY)
        
        return {
            "weather": weather_api,
            "market": market_api,
            "crop_rag": crop_rag,
            "disease": disease_detector,
            "llm": llm,
            "translator": translator
        }
    except Exception as e:
        st.error(f"Failed to initialize components: {e}")
        return None

# Header
st.markdown("""
<div class="header">
    <h1>🌾 Farmer Copilot</h1>
    <p>Your AI-Powered Agricultural Assistant</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.subheader("👤 Your Profile")
    
    location = st.text_input(
        "📍 Location (District, State)",
        placeholder="e.g., Nashik, Maharashtra",
        key="location_input"
    )
    
    current_crop = st.selectbox(
        "🌾 Current Crop",
        ["Select", "Wheat", "Rice", "Cotton", "Sugarcane", "Soybean"]
    )
    
    soil_type = st.selectbox(
        "🌱 Soil Type",
        ["Select", "Black Soil", "Alluvial", "Red Soil", "Laterite"]
    )
    
    language = st.selectbox(
        "🗣️ Language",
        ["English", "Hindi", "Marathi", "Tamil", "Gujarati"]
    )
    
    st.divider()
    
    if st.button("🔄 Clear History"):
        st.session_state.conversation_history = []
        st.success("Conversation cleared!")

# Main Chat Interface
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("💬 Ask Your Agricultural Question")

with col2:
    if st.button("📸 Upload Image"):
        st.session_state.show_upload = True

# Display chat history
if st.session_state.conversation_history:
    st.divider()
    for msg in st.session_state.conversation_history:
        if msg["role"] == "user":
            st.chat_message("user").write(msg["content"])
        else:
            st.chat_message("assistant").write(msg["content"])
    st.divider()

# User Input
user_input = st.chat_input("Type your question in any language...", key="chat_input")

if user_input:
    # Show loading
    with st.spinner("🤔 Analyzing your question..."):
        try:
            # Initialize components
            components = initialize_components()
            
            if components is None:
                st.error("Components not initialized. Check API keys.")
            else:
                # Detect language
                detected_lang = components["translator"].detect_language(user_input)
                
                # Translate to English
                query_en = components["translator"].translate_to_english(user_input, detected_lang)
                
                # Get weather if location provided
                context = {}
                if location:
                    try:
                        context["weather"] = components["weather"].get_weather(location)
                    except:
                        st.warning("Could not fetch weather data")
                
                # Get crop recommendations
                try:
                    context["crops"] = components["crop_rag"].get_recommendations({
                        "N": 200, "P": 40, "K": 300, "pH": 7.2
                    })
                except:
                    pass
                
                # Generate response via LLM
                response_en = components["llm"].generate_response(
                    query_en,
                    context,
                    st.session_state.conversation_history
                )
                
                # Translate back
                response = components["translator"].translate_response(response_en, detected_lang)
                
                # Add to history
                st.session_state.conversation_history.append({
                    "role": "user",
                    "content": user_input
                })
                st.session_state.conversation_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Display response
                st.chat_message("user").write(user_input)
                st.chat_message("assistant").write(response)
                
        except Exception as e:
            st.error(f"Error processing query: {str(e)}")
            logger.error(f"Error: {e}")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: gray; font-size: 12px;'>
    🌾 Farmer Copilot | Powered by AI | Real-Time Market & Weather Data
    <br/>
    Made with ❤️ for Indian Farmers
</div>
""", unsafe_allow_html=True)
