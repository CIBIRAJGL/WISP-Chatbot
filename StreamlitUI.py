# StreamlitUI.py
import streamlit as st
import time
import itertools
from Backend import ask_groq 

# --- Custom CSS for UI Enhancements ---
st.markdown("""
<style>
    /* Main container */
    .stApp {
        background-color: #f5f5f5;
    }
    
    /* Chat messages */
    .stChatMessage {
        border-radius: 15px;
        padding: 12px 18px;
        margin: 8px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* User message */
    [data-testid="stChatMessage"][aria-label="user"] {
        background-color: #e3f2fd;
        margin-left: 15%;
    }
    
    /* Assistant message */
    [data-testid="stChatMessage"][aria-label="assistant"] {
        background-color: #ffffff;
        margin-right: 15%;
    }
    
    /* Input box */
    .stTextInput>div>div>input {
        border-radius: 20px;
        padding: 12px;
    }
    
    /* Sidebar */
    .stSidebar {
        background: linear-gradient(180deg, #4b6cb7 0%, #182848 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- Image URLs ---
logo_url = "https://raw.githubusercontent.com/CIBIRAJGL/WISP/main/Resources/Logo.png"
user_url = "https://raw.githubusercontent.com/CIBIRAJGL/WISP/main/Resources/User.png"

# --- Sidebar Configuration ---
with st.sidebar:
    st.image(logo_url, width=150)
    st.title("Settings")
    
    # Response style selector
    response_style = st.selectbox(
        "Response Style",
        ["Professional", "Friendly", "Concise", "Humorous"],
        index=1
    )
    
    # Model parameters
    with st.expander("Advanced Settings"):
        temperature = st.slider("Creativity", 0.0, 1.0, 0.7)
        max_length = st.slider("Max Response Length", 50, 500, 200)
    
    st.markdown("---")
    st.markdown("💡 Tip: Try uploading files or using voice input!")

# --- Main Chat Interface ---
st.set_page_config(page_title='Wisp!', page_icon=logo_url, layout="wide")

# Header with logo
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo_url, width=80)
with col2:
    st.markdown("# Wisp AI Assistant")
    st.caption("Your intelligent conversational partner")

# --- Session State ---
if 'messages' not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant", 
        "content": "Hello! I'm Wisp. How can I assist you today?"
    })

# --- Display Chat History ---
avatars = {"assistant": logo_url, "user": user_url}

for message in st.session_state.messages:
    with st.chat_message(name=message["role"], avatar=avatars[message["role"]]):
        st.markdown(message["content"])

# --- User Input Area ---
input_col, voice_col = st.columns([10, 1])
with input_col:
    prompt = st.chat_input("Type your message here...")
with voice_col:
    if st.button("🎙️", help="Voice input (coming soon)"):
        st.toast("Voice input feature coming in next update!")

if prompt:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message(name="user", avatar=avatars["user"]):
        st.markdown(prompt)
    
    # Generate and display assistant response
    with st.chat_message(name="assistant", avatar=avatars["assistant"]):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Wisp is thinking..."):
            # Add response style to prompt
            enhanced_prompt = f"Respond in {response_style} style: {prompt}"
            raw_response = ask_groq(enhanced_prompt)
            response = str(raw_response)
            
            # Typing animation
            dots = itertools.cycle(['', '.', '..', '...'])
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.03)
                message_placeholder.markdown(full_response + next(dots), unsafe_allow_html=True)
            
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# --- File Uploader (Bottom of Screen) ---
with st.expander("📁 Upload Files", expanded=False):
    uploaded_file = st.file_uploader(
        "Upload PDF, TXT, or CSV files", 
        type=["pdf", "txt", "csv"],
        label_visibility="collapsed"
    )
    if uploaded_file:
        st.toast(f"File {uploaded_file.name} uploaded successfully!")
