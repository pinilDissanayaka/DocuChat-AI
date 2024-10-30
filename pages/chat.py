import streamlit as st
from document import make_temp_dir, remove_temp_dir, save_documents, load_documents
from vector_store import create_index, load_to_index

temp_dir="document/upload"

st.set_page_config(page_title="DocuChat AI: Your Intelligent Document Assistant", page_icon="📄", layout="wide")


uploaded_file=st.file_uploader("Upload your documents", type=["pdf"], accept_multiple_files=True)

if uploaded_file:
    with st.status(label="Uploading documents..", expanded=True):
        st.write("Make temporary directory..")
        temp_dir=make_temp_dir(temp_dir=temp_dir)
        
        st.write("Saving documents..")
        saved_paths=save_documents(documents=uploaded_file, temp_dir=temp_dir)
        
        st.write("Loading documents..")
        loaded_documents=load_documents(temp_dir=temp_dir)
        
        st.write("Creating index..")
        index_name=create_index(index_name="docuchat", dimension=1536)
        
        st.write("Loading to index..")
        retriever=load_to_index(documents=loaded_documents)
        
        st.write("Removing temporary directory..")
        remove_temp_dir(temp_dir=temp_dir)
