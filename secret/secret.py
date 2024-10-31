import os
import streamlit as st


def load_secret(openai_api_key=None, pinecone_api_key=None):
    try:
        if openai_api_key and pinecone_api_key:
            os.environ["OPENAI_API_KEY"] = openai_api_key
            os.environ["PINECONE_API_KEY"] = pinecone_api_key 
        elif "OPENAI_API_KEY" and "PINECONE_API_KEY" in st.secrets:
            os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
            os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]
    except Exception as e:
        st.error(f"Please provide API keys for Open AI and Pinecone. {e.args}")
    