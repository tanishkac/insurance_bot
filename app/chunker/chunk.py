# app/chunker/chunk.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
import logging

logger = logging.getLogger(__name__)

def chunk_documents(
    pages: List[Document],
    chunk_size: int = 1500,
    chunk_overlap: int = 200
) -> List[Document]:
    """
    Splits documents into chunks using RecursiveCharacterTextSplitter.

    Args:
        pages (List[Document]): Documents to split.
        chunk_size (int): Max characters per chunk.
        chunk_overlap (int): Overlapping characters between chunks.

    Returns:
        List[Document]: List of chunked documents.
    """
    logger.info(f"Splitting {len(pages)} pages into chunks...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_documents(pages)
    logger.info(f"Generated {len(chunks)} chunks.")
    return chunks
