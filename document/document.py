import os
import streamlit as st


def make_temp_dir(temp_dir="document/temp"):
    try:
        if os.path.exists(temp_dir):
            return temp_dir
        else:
            os.makedirs(temp_dir)
            return temp_dir
    except Exception as e:
        st.error(f"Unable to create temp directory. {e.args}")
        
def remove_temp_dir(temp_dir="document/temp"):
    try:
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)
    except Exception as e:
        st.error(f"Unable to remove temp directory. {e.args}")
        
def save_documents(documents, temp_dir="document/temp"):
    try:
        saved_files=[]
        for document in documents:
            saved_path=os.path.join(temp_dir, document.name)
            
            with open(saved_path, "wb") as f:
                f.write(document.read())
                saved_files.append(saved_path)
                
        return saved_files
    except Exception as e:
        st.error(f"Unable to save documents. {e.args}")
        
