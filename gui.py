import streamlit as st
import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()


st.set_page_config(page_title="Daily Affirmations", page_icon="💖", layout="centered")

st.title("💖 Daily Affirmations for My Love 💖")
st.write("Click the button below to get today’s affirmation.")

API_URL = os.getenv("AFFIRMATION_API_URL", "https://your-api.com/affirmation")

# Store affirmation for the day
if "today_affirmation" not in st.session_state or st.session_state["date"] != str(datetime.date.today()):
    st.session_state["today_affirmation"] = None
    st.session_state["date"] = str(datetime.date.today())

if st.button("✨ Get Today’s Affirmation ✨"):
    if not st.session_state["today_affirmation"]:
        try:
            response = requests.get(API_URL, timeout=10)
            if response.status_code == 200:
                data = response.json()
                st.session_state["today_affirmation"] = data.get("affirmation", "You are loved and appreciated 💕")
            else:
                st.session_state["today_affirmation"] = "⚠️ Could not fetch affirmation."
        except Exception as e:
            st.session_state["today_affirmation"] = f"Error: {e}"

# Display affirmation
if st.session_state["today_affirmation"]:
    st.success(st.session_state["today_affirmation"])
