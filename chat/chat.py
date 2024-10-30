from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI
from time import sleep

def chat_with_pdf(question:str, retriever:str):

    question_prompt_template="""
    You are an AI assistant helping users interact with a document. 
    Below is the document context and previous chat history to help you respond to the user's question. 
    Use the document context to provide the most accurate and relevant answer.
    Document Context: {CONTEXT}    
    User's Question: {QUESTION}

    Instructions:
        Analyze the user's question in light of the document context and past interactions.
        Retrieve relevant information from the document context to ensure accuracy.
        If the answer is not clear from the context, 
        provide the best possible response based on document insights and suggest further clarification if needed.
        If the answer is not found in the context, kindly state "I don't know." Don't try to make up an answer.
    Answer:
    """

    question_prompt=ChatPromptTemplate.from_template(question_prompt_template)

    question_chain = (
        {"CONTEXT": RunnablePassthrough(), "QUESTION":RunnablePassthrough()}
        | question_prompt
        | ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        | StrOutputParser()
        )
    
    response=question_chain.invoke({"QUESTION": question, "CONTEXT": retriever})
    
    return response


def stream_chat(response:str, delay=0.05):
    for word in response.split(" "):
        yield word + " "
        sleep(delay)