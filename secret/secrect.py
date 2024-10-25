import os
import streamlit as st


def load_secret(groq_api_key=None, google_api_key=None, pinecone_api_key=None):
    try:
        if groq_api_key and google_api_key and pinecone_api_key:
            os.environ["GROQ_API_KEY"] = groq_api_key
            os.environ["GOOGLE_API_KEY"] = google_api_key
            os.environ["PINECONE_API_KEY"] = pinecone_api_key 
        elif "GROQ_API_KEY" and "GOOGLE_API_KEY" and "PINECONE_API_KEY" in st.secrets:
            os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
            os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
            os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]
    except Exception as e:
        st.error(f"Please provide API keys for GROQ, Google and Pinecone. {e.args}")
    