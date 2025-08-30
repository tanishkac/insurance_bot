# app/utils/chunk_io.py

import json
from langchain_core.documents import Document

def save_chunks(chunks, filepath):
    """Serialize and save Document chunks as JSON."""
    serializable = [
        {"page_content": c.page_content, "metadata": getattr(c, "metadata", {})}
        for c in chunks
    ]
    with open(filepath, "w") as f:
        json.dump(serializable, f)

def load_chunks(filepath):
    """Load Document chunks from JSON."""
    with open(filepath) as f:
        data = json.load(f)
    return [Document(page_content=entry["page_content"], metadata=entry.get("metadata", {})) for entry in data]
