# utils.py (FINAL CORRECTED VERSION)

import streamlit as st
import google.generativeai as genai
import os
from gtts import gTTS
import io

# --- CORRECTED FUNCTION TO HANDLE SECRETS ---
def configure_gemini():
    """
    Configures the Gemini API in a way that works for both local development
    (using .env) and cloud deployment (using st.secrets).
    """
    api_key = None
    # First, try to get the key from Streamlit's secrets (for cloud deployment)
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    # If a FileNotFoundError or KeyError occurs, it means we're likely local
    except (KeyError, FileNotFoundError):
        # Fall back to getting the key from the .env file
        api_key = os.getenv("GOOGLE_API_KEY")

    # If the API key is still not found after both attempts, show an error.
    if not api_key:
        st.error("🚨 Google API Key not found. Please set it in your .env file for local development or in Streamlit secrets for deployment.")
        st.stop()
    
    # Configure the Gemini library with the successfully found key
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"🚨 Error configuring the Gemini API: {e}")
        st.stop()


# --- AI AND PROMPT ENGINEERING ---
INSTRUCTIONAL_PROMPT = """
You are an expert AI Health Advisor. Your goal is to assist users by analyzing their described symptoms. Your response MUST adhere to the following strict rules: 1.  **Mandatory Disclaimer:** You MUST start every single response with the following disclaimer, exactly as written: "**Disclaimer:** I am an AI assistant and not a medical professional. This information is for educational purposes only. Please consult a qualified healthcare provider for any health concerns." 2.  **Structured Response:** After the disclaimer, you must format the rest of your response in Markdown with exactly three sections, using these headers: `### Probable Conditions`, `### Recommended Actions`, `### Dietary Suggestions`. 3.  **Content Guidelines:** Under `### Probable Conditions`, list potential conditions without giving a definitive diagnosis. Under `### Recommended Actions`, suggest safe steps, prioritizing seeing a doctor. Under `### Dietary Suggestions`, provide simple, healthy food recommendations. Analyze the user's query and generate a response that follows these instructions perfectly.
"""

def get_gemini_response_stream(question: str):
    """Calls Gemini and streams the response."""
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    try:
        response_stream = model.generate_content(
            [INSTRUCTIONAL_PROMPT, question],
            stream=True,
            generation_config=genai.types.GenerationConfig(temperature=0.7)
        )
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        yield f"An error occurred while communicating with the AI: {str(e)}"

# --- UI HELPER FUNCTIONS ---
def display_response_in_tabs(response_text: str):
    """Parses the AI's response and displays it in tabs with an audio player."""
    try:
        parts = response_text.split("###")
        disclaimer = parts[0].strip()
        conditions = "###" + parts[1].strip()
        actions = "###" + parts[2].strip()
        diet = "###" + parts[3].strip()

        st.markdown(disclaimer)
        
        tab1, tab2, tab3 = st.tabs(["Probable Conditions", "Recommended Actions", "Dietary Suggestions"])
        with tab1:
            st.markdown(conditions, unsafe_allow_html=True)
        with tab2:
            st.markdown(actions, unsafe_allow_html=True)
        with tab3:
            st.markdown(diet, unsafe_allow_html=True)

        generate_audio_player(response_text)
    except IndexError:
        st.warning("AI response format was unexpected. Displaying raw text.")
        st.markdown(response_text)
        generate_audio_player(response_text)

def generate_audio_player(text: str):
    """Generates an st.audio player from text using gTTS."""
    try:
        sound_file = io.BytesIO()
        tts = gTTS(text=text, lang='en')
        tts.write_to_fp(sound_file)
        st.audio(sound_file, format='audio/mp3', start_time=0)
    except Exception as e:
        st.error(f"Could not generate audio: {e}")