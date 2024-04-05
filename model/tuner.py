import os
from merger import PDF_DIR, MERGED_PDF_FILENAME, merger_runner
from PyPDF2 import PdfReader
from dotenv import load_dotenv


ENV_DIR = os.path.join(os.getcwd(), '.env')
PDF_DOC = os.path.join(PDF_DIR, MERGED_PDF_FILENAME)

load_dotenv(ENV_DIR)

HF_HUB_TOKEN = os.getenv('HUGGING_FACE_HUB_READ_TOKE')


def get_pdf_text(pdf) -> str:
    text = ""
    pdf_reader = PdfReader(pdf)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


def main():
    raw_text = get_pdf_text(PDF_DOC)
    # file = open('text_pdf.txt', 'w+')
    # file.writelines(raw_text)
    # file.close()


if __name__ == "__main__":
    main()
