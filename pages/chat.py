import streamlit as st
from document import make_temp_dir, remove_temp_dir, save_documents, load_documents



st.set_page_config(page_title="DocuChat AI: Your Intelligent Document Assistant", page_icon="📄", layout="wide")


uploaded_file=st.file_uploader("Upload your documents", type=["pdf", "docx", "txt"], accept_multiple_files=True)

if uploaded_file is not None:
    with st.success("Documents uploaded"):
        temp_dir=make_temp_dir()
        temp_dir=save_documents(uploaded_file, temp_dir)
        documents=load_documents(temp_dir)
        remove_temp_dir(temp_dir)
    
        st.write(len(documents), "documents uploaded")
    
        st.markdown(documents)