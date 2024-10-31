import streamlit as st
from secret import load_secret
from document import make_temp_dir, remove_temp_dir, save_documents, load_documents
from vector_store import create_index, load_to_index
from chat import chat_with_pdf, stream_chat
import traceback

temp_dir="document/upload"

st.set_page_config(page_title="DocuChat AI: Your Intelligent Document Assistant", page_icon="📄", layout="wide")

with st.sidebar:
    st.title("Chat with your documents")
    st.write("""Upload your documents and ask any question. 
             DocuChat AI will search through them to provide you with precise, 
             context-aware responses.""")
    
    if not "OPENAI_API_KEY" and "PINECONE_API_KEY" in st.secrets:
        openai_api_key = st.text_input("Open AI API Key", type="password")
        pinecone_api_key = st.text_input("Pinecone API Key", type="password")
        
        load_secret(openai_api_key=openai_api_key, pinecone_api_key=pinecone_api_key)
    
    if st.button("Reset"):
        if "messages" in st.session_state.keys():
            st.session_state.clear()
            

    uploaded_files=st.file_uploader("Upload your documents", type=["pdf"], accept_multiple_files=True)
    
    if "uploaded_files" not in st.session_state.keys():
        st.session_state["uploaded_files"] = uploaded_files
        
    if uploaded_files:
        if st.button("Upload"):
            if "upload_status" not in st.session_state.keys():
                st.session_state["upload_status"] = True
        


if "upload_status" in st.session_state.keys():
    if st.session_state["upload_status"]:
        with st.status(label="Uploading documents..", expanded=False):
            temp_dir=make_temp_dir(temp_dir=temp_dir)
            
            st.write("Saving documents..")
            saved_paths=save_documents(documents=uploaded_files, temp_dir=temp_dir)
            
            st.write("Loading documents..")
            loaded_documents=load_documents(temp_dir=temp_dir)
            
            index_name=create_index()
            
            st.write("Loading to index..")
            
            load_to_index(documents=loaded_documents)
            
            remove_temp_dir(temp_dir=temp_dir)
        
if "OPENAI_API_KEY" and "PINECONE_API_KEY" in st.secrets:
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you? 👋"}]


    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    if st.session_state.messages[-1]["role"] != "assistant":
        try:
            retriever=st
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = chat_with_pdf(question=prompt)
                    st.write_stream(stream=stream_chat(response=response))
                    
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
        except Exception as e:
            st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")
            st.exception(f"{traceback.format_exc()}")
else:
    st.error("Please provide API keys for Open AI and Pinecone.", icon="🚨")