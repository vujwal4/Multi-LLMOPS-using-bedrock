import streamlit as st
import requests
from APP.config.settings import settings
from APP.common.log import get_logger
from APP.common.exception import CustomException

logger = get_logger(__name__)

st.set_page_config(page_title="Multi Al Agent", layout="centered")
st.title("Multi AI Agent LLMOps")

st.markdown("""
    <style>
    /* 1. Background Gradient */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    
    /* 2. Style the Main Title */
    h1 {
        color: #00d4ff;
        text-shadow: 2px 2px 4px #000000;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 3. Style Input Boxes */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid #00d4ff !important;
    }

    /* 4. Style the "Ask Agent" Button */
    div.stButton > button:first-child {
        background-color: #00d4ff;
        color: black;
        border-radius: 10px;
        width: 100%;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #008fb3;
        color: white;
        border: 1px solid white;
    }

    /* 5. Custom Agent Response Box */
    .agent-response {
        background-color: rgba(0, 212, 255, 0.1);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

system_prompt = st.text_area("Define your AI Agent:", height=70)
st.info("🤖 Model using: amazon.nova-lite-v1:0 from Amazon Bedrock")
selected_model = "amazon.nova-lite-v1:0" 

allow_web_search = st.checkbox("Allow web search")

user_query = st.text_area("Enter your query", height=150)

API_URL="http://127.0.0.1:9999/chat"

if st.button("Ask Agent") and user_query.strip():
    payload = {
    "model_name" : selected_model,
    "system_prompt" : system_prompt,
    "messages": [user_query],
    "allow_search" : allow_web_search
    }
    try:
        logger.info("Sending request to backend")
        response = requests.post(API_URL, json=payload)
        if response.status_code==200:
            agent_response = response.json().get("response","")
            logger.info("Sucesfully recived response from backend")
            st.subheader("Agent Response")
            st.markdown(agent_response.replace("\n", "<br>"), unsafe_allow_html=True)
        else:
            logger.error("Backend error")
            st.error("Error with backend")
    except Exception as e:
        logger.error("Error occured while sending request to backend")
        logger.error(f"Error: {e}")
        st.error(f"Failed to communicate to backend | Details: {e}")
