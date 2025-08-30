import re
from typing import List, Optional
from langchain_core.documents import Document
from app.utils.logger import get_logger
from app.utils.extract_page import extract_page_numbers

logger = get_logger(__name__)


def get_relevant_chunks(question: str, 
                         all_chunks: List[Document], 
                         vectorstore, 
                         top_k: int = 5) -> List[Document]:
    """
    Returns relevant chunks based on semantic similarity and optional page filtering.
    """
    logger.info(f"Retrieving top {top_k} relevant chunks for question: '{question}'")
    retriever = vectorstore.as_retriever(search_type="similarity", k=top_k)
    relevant_chunks = retriever.invoke(question)

    referenced_pages = extract_page_numbers(question)

    if not referenced_pages:
        logger.info("No page numbers found in question; using semantic results.")
        return relevant_chunks

    filtered_chunks = [
        chunk for chunk in all_chunks
        if int(chunk.metadata.get("page", -1)) in referenced_pages or
           str(chunk.metadata.get("page_label", "")) in map(str, referenced_pages)
    ]

    logger.info(f"Filtered {len(filtered_chunks)} chunks based on page references: {referenced_pages}")

    if not filtered_chunks:
        logger.warning("No chunks matched the page references; falling back to semantic results.")

    if filtered_chunks: 
        print(filtered_chunks)
        logger.info("Filtered chunks based on page references:")
    else:
        print(relevant_chunks)
        logger.info("Returning relevant chunks based on semantic similarity without page filtering.")

    return filtered_chunks if filtered_chunks else relevant_chunks
