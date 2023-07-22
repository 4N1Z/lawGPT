
import os
from pdf2docx import Converter
from docx2rtf import Converter as RTFConverter

def convert_pdf_to_rtf(pdf_folder, rtf_folder):
    # Iterate over PDF files in the folder
    for file_name in os.listdir(pdf_folder):
        if file_name.endswith('.pdf'):
            pdf_path = os.path.join(pdf_folder, file_name)
            docx_path = os.path.join(rtf_folder, os.path.splitext(file_name)[0] + '.docx')
            rtf_path = os.path.join(rtf_folder, os.path.splitext(file_name)[0] + '.rtf')

            # Convert PDF to DOCX
            cv = Converter(pdf_path)
            cv.convert(docx_path)
            cv.close()

            # Convert DOCX to RTF
            rtf_cv = RTFConverter(docx_path)
            rtf_cv.convert(rtf_path)
            rtf_cv.close()

            print(f"Converted {pdf_path} to {rtf_path}")

# Usage
pdf_folder = '/path/to/pdf_folder'
rtf_folder = '/path/to/rtf_folder'

convert_pdf_to_rtf(pdf_folder, rtf_folder)