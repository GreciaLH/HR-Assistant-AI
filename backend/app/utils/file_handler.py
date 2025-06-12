import os
import uuid
from fastapi import UploadFile
import shutil
import PyPDF2
import docx
import io

async def save_upload_file(upload_file: UploadFile, destination: str) -> str:
    """
    Save an uploaded file to the specified destination directory
    Returns the path to the saved file
    """
    # Crear un nombre de archivo único
    filename = f"{uuid.uuid4()}_{upload_file.filename}"
    file_path = os.path.join(destination, filename)
    
    # Asegurar que el directorio de destino existe
    os.makedirs(destination, exist_ok=True)
    
    # Guardar el archivo
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return file_path

async def extract_text_from_file(file_path: str) -> str:
    """
    Extract text content from a file (PDF or DOCX)
    Returns the extracted text
    """
    file_extension = os.path.splitext(file_path)[1].lower()
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_path)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_path)
    else:
        # Para otros tipos de archivo, intentar leer como texto
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            return f"Could not extract text from file: {str(e)}"

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        text = f"Error extracting text from PDF: {str(e)}"
    
    return text

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file"""
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        text = f"Error extracting text from DOCX: {str(e)}"
    
    return text