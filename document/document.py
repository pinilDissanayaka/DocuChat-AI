import os
import shutil
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_core.documents import Document

def make_temp_dir(temp_dir):
    try:
        if os.path.exists(temp_dir):
            return temp_dir
        else:
            os.makedirs(temp_dir)
            return temp_dir
    except Exception as e:
        st.error(f"Unable to create temp directory. {e.args}")
        
def remove_temp_dir(temp_dir):
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    except Exception as e:
        st.error(f"Unable to remove temp directory. {e.args}")
        
def save_documents(documents, temp_dir):
    try:
        for document in documents:
            saved_path=os.path.join(temp_dir, document.name)
            
            with open(saved_path, "wb") as f:
                f.write(document.read())
    
        return temp_dir
    except Exception as e:
        st.error(f"Unable to save documents. {e.args}")
        
def load_documents(temp_dir):
    try:
        loaded_documents=DirectoryLoader(path=temp_dir, silent_errors=True, loader_cls=PyPDFLoader).load()
        
        return loaded_documents
    except Exception as e:
        st.error(f"Unable to load documents. {e.args}")