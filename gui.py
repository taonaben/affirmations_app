import streamlit as st
import requests
import datetime
import os
from dotenv import load_dotenv

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
        background-image: url("https://whvn.cc/ymxz7x");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    
    /* Optional: Add overlay for better text readability */
    .stApp::before {
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
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 2rem;
        margin-top: 2rem;
    }
    
    /* Optional: Style the title */
    h1 {
        text-align: center;
        color: #333;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align: center;'>Here when I can't be there</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center;'>Click the button below to enter my heart.</p>",
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
            try:
                response = requests.get(API_URL, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    st.session_state["today_affirmation"] = data.get(
                        "affirmation", "You are loved and appreciated 💕"
                    )
                else:
                    st.session_state["today_affirmation"] = (
                        "⚠️ Ooops, I’m sorry I disappointed you. You can try again later."
                    )
            except Exception as e:
                st.session_state["today_affirmation"] = f"Error: {e}"


# Display affirmation
if st.session_state["today_affirmation"]:
    st.success(st.session_state["today_affirmation"])
