from ollama import AsyncClient
import asyncio
import os
import sys
from merger import PDF_DIR, MERGED_PDF_FILENAME, merger_runner
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain_community.llms import Ollama
# import ollama
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
# from langchain_community.embeddings import HuggingFaceInstructEmbeddings
# from langchain_community.vectorstores import chroma
# from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
# from langchain_community.chat_models import ChatOllama
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser
# import huggingface_hub
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.llms import HuggingFaceHub
# # from langchain_community import embeddings
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA


ENV_DIR = os.path.join(os.getcwd(), '.env')
PDF_DOC = os.path.join(PDF_DIR, MERGED_PDF_FILENAME)

load_dotenv(ENV_DIR)

HF_HUB_TOKEN = os.getenv('HUGGING_FACE_HUB_READ_TOKE')


def get_pdf_text(pdf) -> str:
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return ''.join(text.splitlines())
    # return text


if __name__ == "__main__":
    ollama = Ollama(base_url='http://localhost:11434', model='llama2')

    loader = PyPDFLoader(PDF_DOC)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(separators=["\n", "\n\n", " "],
                                                                         chunk_size=500, chunk_overlap=20)
    text = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(
        documents=text, embedding=GPT4AllEmbeddings())

    # qachain = RetrievalQA.from_chain_type(
    #     ollama, retriver=vectorstore.as_retriever())

    # q = "what is Inheritance Tax?"
    qa_chain = ConversationalRetrievalChain.from_llm(
        ollama,
        retriever=vectorstore.as_retriever(),
        return_source_documents=False
    )

    chat_history = []
    while True:
        query = input('Prompt: ')
        if query.lower() in ["exit", "quit", "q"]:
            print('Exiting')
            sys.exit()
        result = qa_chain({'question': query, 'chat_history': chat_history})
        print('Answer: ' + result['answer'] + '\n')
        chat_history.append((query, result['answer']))
    # async def chat():
    #     message = {'role': 'user', 'content': 'Why is the sky blue?'}
    #     async for part in await AsyncClient().chat(model='llama2', messages=[message], stream=True):
    #         print(part['message']['content'], end='', flush=True)

    # asyncio.run(chat())
