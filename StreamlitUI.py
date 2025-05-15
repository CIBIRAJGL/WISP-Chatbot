# StreamlitUI.py

import streamlit as st
import time
import itertools
from Backend import ask_groq 

# --- Image URLs from GitHub (RAW links) ---
logo_url = "https://raw.githubusercontent.com/CIBIRAJGL/WISP/main/Resources/Logo.png"
user_url = "https://raw.githubusercontent.com/CIBIRAJGL/WISP/main/Resources/User.png"

# --- Streamlit Page Setup ---
st.set_page_config(page_title='Wisp!', page_icon=logo_url)
st.markdown("# Hey Wisp! 🤖")

# --- Session State for Conversation ---
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- Avatar Configuration ---
avatars = {"assistant": logo_url, "user": user_url}

# --- Initial Greeting from Wisp ---
with st.chat_message(name="assistant", avatar=avatars["assistant"]):
    st.markdown("### Ask your Queries!")

# --- Display Existing Chat History ---
for message in st.session_state.messages:
    with st.chat_message(name=message["role"], avatar=avatars[message["role"]]):
        st.markdown(message["content"])

# --- Input Box for User ---
if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user's message
    with st.chat_message(name="user", avatar=avatars["user"]):
        st.markdown(prompt)

    # Placeholder for assistant response
    with st.chat_message(name="assistant", avatar=avatars["assistant"]):
        message_placeholder = st.empty()
        full_response = ""

        # Typing effect with a spinner
        with st.spinner(text="Thinking... 💭💭💭"):
            raw_response = ask_groq(prompt) 
            response = str(raw_response)

            # Typing animation effect
            dots = itertools.cycle(['', '.', '..', '...'])
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + next(dots), unsafe_allow_html=True)

            # Final display of full message
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
