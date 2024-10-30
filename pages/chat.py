import streamlit as st
from document import make_temp_dir, remove_temp_dir, save_documents, load_documents
from vector_store import create_index, load_to_index, connect_to_index
from chat import chat_with_pdf

temp_dir="document/upload"

st.set_page_config(page_title="DocuChat AI: Your Intelligent Document Assistant", page_icon="📄", layout="wide")


uploaded_file=st.file_uploader("Upload your documents", type=["pdf"], accept_multiple_files=True)


if uploaded_file:
    with st.status(label="Uploading documents..", expanded=True):
        temp_dir=make_temp_dir(temp_dir=temp_dir)
        
        st.write("Saving documents..")
        saved_paths=save_documents(documents=uploaded_file, temp_dir=temp_dir)
        
        st.write("Loading documents..")
        loaded_documents=load_documents(temp_dir=temp_dir)
        
        index_name=create_index()
        
        st.write("Loading to index..")
        
        retriever=load_to_index(documents=loaded_documents)
        
        if "retriever" not in st.session_state.keys():
            st.session_state.retriever = retriever
        
        remove_temp_dir(temp_dir=temp_dir)
        
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
                if "retriever" not in st.session_state.keys():
                    retriever = connect_to_index()
                    st.session_state.retriever = retriever
                else:
                    response = chat_with_pdf(question=prompt, index_name=index_name, retriever=retriever)
                
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
    except Exception as e:
        st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")
