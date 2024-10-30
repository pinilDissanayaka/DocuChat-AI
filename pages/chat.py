import streamlit as st
from document import make_temp_dir, remove_temp_dir, save_documents, load_documents
from vector_store import create_index, load_to_index, get_retriever
from chat import chat_with_pdf, stream_chat

temp_dir="document/upload"

st.set_page_config(page_title="DocuChat AI: Your Intelligent Document Assistant", page_icon="📄", layout="wide")

with st.sidebar:
    st.title("Chat with your documents")
    st.write("""Upload your documents and ask any question. 
             DocuChat AI will search through them to provide you with precise, 
             context-aware responses.""")
    
    if st.button("Reset"):
        if "messages" in st.session_state.keys():
            st.session_state.clear()
        


uploaded_file=st.file_uploader("Upload your documents", type=["pdf"], accept_multiple_files=True)


if uploaded_file:
    if st.button("Upload"):
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
                response = chat_with_pdf(question=prompt)
                st.write_stream(stream=stream_chat(response=response))
                
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)
    except Exception as e:
        st.warning(f"An unexpected error occurred: {str(e.args)}. Please try again.", icon="⚠️")
