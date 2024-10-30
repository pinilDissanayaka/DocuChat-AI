from langchain_pinecone.vectorstores import PineconeVectorStore
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec
import streamlit as st
from time import sleep

def create_index(index_name="docuchat", dimension=1536):
    try:
        pinecone=Pinecone()
        
        existing_indexes=pinecone.list_indexes().names()
        
        if not index_name in existing_indexes:
            pinecone.create_index(name=index_name, 
                                dimension=dimension, 
                                metric="cosine",
                                spec=ServerlessSpec(
                                    cloud="aws", 
                                    region="us-east-1"
                                    )
                                )
            
            while not pinecone.describe_index(index_name).status["ready"]:
                sleep(3)
                
        return index_name
    except Exception as e:
        st.exception(f"Unable to create index. {e.args}")


def load_to_index(documents, index_name, chunk_size=1100, chunk_overlap=450, embedding_model="text-embedding-3-large"):
    try:
        splitted_documents=RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap).split_documents(documents)
        
        embedding_model=OpenAIEmbeddings(model=embedding_model)
        
        vector_store=PineconeVectorStore(
            index_name=index_name,
            embedding=embedding_model
        )
        
        vector_store.from_documents(documents=splitted_documents, embedding=embedding_model)
        
        retriever=vector_store.as_retriever()
        
        return retriever
    except Exception as e:
        st.exception(f"Unable load documents to index. {e.args}")