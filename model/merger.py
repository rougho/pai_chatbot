import os
from PyPDF2 import PdfWriter

PARRENT_DIR = os.getcwd()
CHILD_DIRS = [dir for dir in os.listdir(
    PARRENT_DIR) if os.path.isdir(os.path.join(PARRENT_DIR, dir))]
MODEL_DIR = os.path.join(PARRENT_DIR, "model")
DATA_DIR = os.path.join(MODEL_DIR, "data")
PDF_DIR = os.path.join(DATA_DIR, "pdf")
PDF_FILES = list()
MERGED_PDF_FILENAME = 'merged.pdf'


def data_directory_handler():
    try:
        os.makedirs(DATA_DIR)
        print(f"{DATA_DIR} created.")
    except FileExistsError:
        print(f"{DATA_DIR} existed but was a symbolic link.")


def pdf_directory_handler():
    try:
        os.makedirs(os.path.join(DATA_DIR, PDF_DIR))
        print(f"{PDF_DIR} created.")
    except FileExistsError:
        print(f"{PDF_DIR} existed but was a symbolic link.")


# def check_direcotry_before_merge():
#     PDF_FILES = [pdf for pdf in os.listdir(PDF_DIR) if pdf.endswith(
#         '.pdf') and pdf != MERGED_PDF_FILENAME]
#     if len(PDF_FILES) == 0:
#         return False
#     return PDF_FILES


def exctract_pdf_files(dir_path: str) -> tuple[list, int]:
    try:
        files = os.listdir(dir_path)
        pdfs = [pdf for pdf in files if pdf.endswith('.pdf')]
        number_of_files = len(pdfs)
        return pdfs, number_of_files
    except FileNotFoundError:
        return [], -1


def pdf_merger(dir_path):

    pdfs_list, number_of_pdfs = exctract_pdf_files(PDF_DIR)
    if number_of_pdfs == -1:
        print("Error extract pdf files")
        return False
    else:
        merger = PdfWriter()

        for pdf in pdfs_list:
            merger.append(f"{PDF_DIR}/{pdf}")

        merger.write(f"{PDF_DIR}/{MERGED_PDF_FILENAME}")
        merger.close()
        print(f"{' '.join(pdfs_list)} has been merged.")
        return True


def merger_runner():
    data_directory_handler()
    pdf_directory_handler()
    pdf_merger(PDF_DIR)
