# pages/1_🩺_Health_Advisor_Chat.py

import streamlit as st
from dotenv import load_dotenv
from utils import configure_gemini, get_gemini_response_stream, display_response_in_tabs

# Load environment variables and configure API at the start
load_dotenv()
configure_gemini()

# --- STREAMLIT PAGE LAYOUT ---
st.title("💬 Health Advisor Chat")
st.info("Describe your symptoms below. The AI will analyze them and provide structured guidance.", icon="🧑‍⚕️")

# Initialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat messages from history consistently
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            display_response_in_tabs(message["content"])
        else:
            st.markdown(message["content"])

# Handle new user input
if user_input := st.chat_input("I have a persistent cough and slight fever..."):
    # Add user message to history and display it
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get and display AI response with streaming for better UX
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Stream the raw response for a live "typing" effect
        stream_generator = get_gemini_response_stream(user_input)
        full_response = response_placeholder.write_stream(stream_generator)
        
        # Once streaming is complete, clear the placeholder and display the final formatted tabs
        response_placeholder.empty()
        display_response_in_tabs(full_response)
            
    # Add the complete AI response to history for consistent display later
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})