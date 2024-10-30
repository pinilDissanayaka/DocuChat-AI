from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_openai.chat_models import ChatOpenAI
from time import sleep

def chat_with_pdf(question:str, retriever:str):

    question_prompt_template= """Given the following context and a question, 
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

    question_chain = (
        {"CONTEXT": RunnablePassthrough(), "QUESTION":RunnablePassthrough()}
        | question_prompt
        | ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
        | StrOutputParser()
        )
    
    response=question_chain.invoke({"CONTEXT": retriever, "QUESTION": question})
    
    return response


def stream_chat(response:str, delay=0.05):
    for word in response.split(" "):
        yield word + " "
        sleep(delay)