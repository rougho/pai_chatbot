import os
from merger import PDF_DIR, MERGED_PDF_FILENAME, merger_runner
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_community.chat_models import ollama

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


def get_text_chunks(text):
    spliter = RecursiveCharacterTextSplitter(
        # separators="\n",
        separators=" ",
        chunk_size=1000,
        chunk_overlap=100,
        length_function=len,
    )
    chunks = spliter.split_text(text)
    return chunks


def get_vectorestore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(
        model_name="hkunlp/instructor-xl")

    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)

    return vectorstore


def get_coversation_chain(vectorstore):
    llm = ollama()
    memory = ConversationBufferMemory(
        memory_key='chat history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def main():
    raw_text = get_pdf_text(PDF_DOC)
    text_chunks = get_text_chunks(raw_text)
    vectorstore = get_vectorestore(text_chunks)
    conversation = get_coversation_chain(vectorstore)

    print("Welcome! Chat with the embedded model. Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        response = conversation(user_input)
        print("Model:", response)


if __name__ == "__main__":
    main()
