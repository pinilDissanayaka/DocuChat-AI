import os
import shutil
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader

temp_dir="document/upload"
def make_temp_dir(temp_dir=temp_dir):
    try:
        if os.path.exists(temp_dir):
            return temp_dir
        else:
            os.makedirs(temp_dir)
            return temp_dir
    except Exception as e:
        st.error(f"Unable to create temp directory. {e.args}")
        
def remove_temp_dir(temp_dir=temp_dir):
    try:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    except Exception as e:
        st.error(f"Unable to remove temp directory. {e.args}")
        
def save_documents(documents, temp_dir=temp_dir):
    try:
        saved_paths=[]
        for document in documents:
            saved_path=os.path.join(temp_dir, document.name)
            
            with open(saved_path, "wb") as f:
                f.write(document.read())
                saved_paths.append(saved_path)
        return saved_paths
    except Exception as e:
        st.error(f"Unable to save documents. {e.args}")
        
def load_documents(saved_paths):
    try:
        loaded_documents=[]
        for saved_path in saved_paths:
            loaded_documents.append(PyPDFLoader(saved_path).load())
            
        return load_documents
    except Exception as e:
        st.error(f"Unable to load documents. {e.args}")