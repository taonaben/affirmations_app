import streamlit as st
import requests
import datetime
import os
from dotenv import load_dotenv
import time

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

load_dotenv()


st.set_page_config(
    page_title="Daily Affirmations",
    page_icon="💖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Enhanced custom background image CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        min-height: 100vh;
    }
    
    /* Fallback background image */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.7;
        z-index: -1;
    }
    
    /* Add overlay for better text readability */
    .stApp::after {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.3);
        z-index: -1;
    }
    
    /* Style the main content area */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Style the title */
    h1 {
        text-align: center;
        color: #333;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    /* Style buttons */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align: center;'>💕 Here when I can't be there 💕</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center;'>Click the button below to enter my heart❤️.</p>",
    unsafe_allow_html=True,
)
# API_URL = os.getenv("AFFIRMATION_API_URL", "https://your-api.com/affirmation")

API_URL = st.secrets["AFFIRMATION_API_URL"]

# Store affirmation for the day
if "today_affirmation" not in st.session_state or st.session_state["date"] != str(
    datetime.date.today()
):
    st.session_state["today_affirmation"] = None
    st.session_state["date"] = str(datetime.date.today())

# Create 3 columns: left, center, right
col1, col2, col3 = st.columns([1, 2, 1])

with col2:  # Put button in the middle column
    if st.button("✨ Make me talk ✨"):
        if not st.session_state["today_affirmation"]:
            # Show loading message
            loading_placeholder = st.empty()
            loading_placeholder.info("Waking up the server… hang tight 💕")

            success = False
            for attempt in range(MAX_RETRIES):
                try:
                    response = requests.get(API_URL, timeout=40)
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state["today_affirmation"] = data.get(
                            "affirmation", "You are loved and appreciated 💕"
                        )
                        success = True
                        break
                    else:
                        if attempt == MAX_RETRIES - 1:  # Last attempt
                            st.session_state["today_affirmation"] = (
                                "⚠️ Ooops, I'm sorry I disappointed you. You can try again later."
                            )
                except Exception as e:
                    if attempt == MAX_RETRIES - 1:  # Last attempt
                        st.session_state["today_affirmation"] = f"Error: {e}"
                    else:
                        time.sleep(RETRY_DELAY)  # wait then retry

            # Clear loading message
            loading_placeholder.empty()


# Display affirmation
if st.session_state["today_affirmation"]:
    st.success(st.session_state["today_affirmation"])
