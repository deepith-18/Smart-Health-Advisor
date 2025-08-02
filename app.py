# app.py (FINAL, WORKING VERSION)

import streamlit as st
import json
from streamlit_lottie import st_lottie

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Smart Health Advisor",
    page_icon="🩺",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- FUNCTION TO LOAD THE LOCAL ANIMATION FILE ---
def load_lottie_file(filepath: str):
    """Loads a Lottie file from a specified filepath."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return None if file is not found or is invalid
        return None

# --- HOME PAGE CONTENT ---
st.title("Welcome to the Smart Health Advisor 🩺")
st.markdown("Your AI-powered assistant for preliminary health symptom analysis.")
st.markdown("---")

col1, col2 = st.columns([1, 1.2])

with col1:
    # Load the lottie animation
    lottie_animation = load_lottie_file("animation.json")
    
    if lottie_animation:
        st_lottie(
            lottie_animation,
            speed=1,
            reverse=False,
            loop=True,
            quality="high", # Options: low, medium, high
            height=200,
            width=200,
            key="health_animation" # A unique key is important
        )
    else:
        # This will only show if animation.json is missing or corrupted
        st.warning("Animation file could not be loaded. Please ensure `animation.json` is in the project folder.")

with col2:
    st.subheader("How It Works")
    st.markdown("""
    1.  Navigate to the **Health Advisor Chat** page.
    2.  Describe your symptoms in the chat box.
    3.  Our AI will provide a structured response.
    """)
    st.warning("**Disclaimer:** This is for informational purposes only and is not a substitute for professional medical advice.", icon="⚠️")

st.markdown("---")
st.info("👈 **Select a page from the sidebar to get started!**")