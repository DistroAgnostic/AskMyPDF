__import__("pysqlite3")
import sys
sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

import os
import streamlit as st
import google.generativeai as genai
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.callbacks.base import BaseCallbackHandler

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

st.title("📄 AskMyPDF – Chat with Any PDF Using LangChain")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    loader = PyPDFLoader("temp.pdf")
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=20
    )
    docs = text_splitter.split_documents(data)

    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"), 
persist_directory=None
    )
    retriever = vectorstore.as_retriever(search_type="similarity")

    prompt = ChatPromptTemplate.from_template(
        """You are my personal assistant to help me talk with the PDF. 
        Use the following context and the conversation history to answer the question.

        Conversation history:
        {chat_history}

        Context:
        {context}

        Question: {input}"""
    )

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    query = st.chat_input("Ask me anything about the PDF:")

    if query:
        with st.spinner("Thinking..."):
            container = st.empty()
            stream_handler = StreamHandler(container)

            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-pro",
                streaming=True,
                callbacks=[stream_handler],
            )

            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)

            history_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.chat_history])

            response = rag_chain.invoke({
                "input": query,
                "chat_history": history_text
            })
 st.session_state.chat_history.append((query, response.get("answer", "")))

    # Show chat history
    if st.session_state.chat_history:
        st.write("### Chat History")
        for q, a in st.session_state.chat_history:
            st.markdown(f"**Q:** {q}")
            st.markdown(f"**A:** {a}")
else:
    st.info("👆 Upload a PDF to get started")