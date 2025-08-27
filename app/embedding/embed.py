# app/embedding/embed.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import uuid
import shutil
import os
import logging

logger = logging.getLogger(__name__)


def get_embedding_function():
    """Returns a HuggingFace embedding function."""
    logger.info("Loading embedding model: all-MiniLM-L6-v2")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return embeddings


def create_vectorstore(chunks, embedding_function, vectorstore_path):
    """Creates a persistent Chroma vector store from text chunks."""
    logger.info("Creating vector store at %s", vectorstore_path)

    ids = [str(uuid.uuid5(uuid.NAMESPACE_DNS, doc.page_content)) for doc in chunks]

    unique_ids = set()
    unique_chunks = []

    for chunk, id in zip(chunks, ids):
        if id not in unique_ids:
            unique_ids.add(id)
            unique_chunks.append(chunk)

    vectorstore = Chroma.from_documents(
        documents=unique_chunks,
        ids=list(unique_ids),
        embedding=embedding_function,
        persist_directory=vectorstore_path
    )
    logger.info("Vector store created and persisted with %d documents", len(unique_chunks))

    return vectorstore



def load_vectorstore(vectorstore_path, embedding_function=None):
    """
    Loads a persisted Chroma vectorstore from the given directory path.
    Requires an embedding function matching the one used during creation.
    """
    if embedding_function is None:
        embedding_function = get_embedding_function()
    
    vectorstore = Chroma(
        persist_directory=vectorstore_path,
        embedding_function=embedding_function
    )
    return vectorstore


def delete_vectorstore(vectorstore_path):
    if os.path.exists(vectorstore_path):
        shutil.rmtree(vectorstore_path)
        logger.info("Deleted vector store at %s", vectorstore_path)