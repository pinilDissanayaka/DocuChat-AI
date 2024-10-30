from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from time import sleep
from vector_store import get_retriever

def chat_with_pdf(question:str):
    question_prompt_template="""Given the following context and a question, 
    generate an answer based on this context only.
    In the answer try to provide as much text as possible from "ANSWER" 
    section in the source document context without making much changes.
    If the answer is not found in the context, kindly state "I don't know." 
    Don't try to make up an answer.

        CONTEXT: {CONTEXT}

        QUESTION: {QUESTION}
    
        ANSWER:
    """

    question_prompt=ChatPromptTemplate.from_template(question_prompt_template)
    
    retriever=get_retriever()

    chain = (
    {"QUESTION":RunnablePassthrough(), "CONTEXT": retriever}
    | question_prompt
    | ChatOpenAI(model="gpt-3.5-turbo")
    | StrOutputParser()
    )
        
    response=chain.invoke(question)
    
    return response


def stream_chat(response:str, delay=0.05):
    for word in response.split(" "):
        yield word + " "
        sleep(delay)