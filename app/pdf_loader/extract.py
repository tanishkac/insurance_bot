# app/pdf_loader/extract.py

from langchain_community.document_loaders import PyPDFLoader
from typing import List
from langchain.schema import Document
from app.utils.logger import get_logger

logger = get_logger(__name__)

def load_pdf(file_path: str) -> List[Document]:
    """
    Loads a PDF file and returns a list of Document pages.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        List[Document]: A list of page-level Document objects.
    """
    try:
        logger.info(f"Attempting to load PDF from: {file_path}")
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        logger.info(f"Successfully loaded {len(pages)} pages from {file_path}")
        return pages
    except Exception as e:
        logger.error(f"Error loading PDF: {e}")
        raise
