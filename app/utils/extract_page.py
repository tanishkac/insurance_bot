import re
from typing import List, Optional
from langchain_core.documents import Document
from app.utils.logger import get_logger

logger = get_logger(__name__)

def extract_page_numbers(question: str) -> List[int]:
    """
    Extracts single pages, comma-separated pages, or ranges (e.g., page 3, pages 4 and 5, p. 2-4)
    """
    pattern = r'(?:page|pg|p)\.?\s*(\d+(?:\s*(?:,|and)\s*\d+)*|\d+\s*-\s*\d+)'  # Match page references
    matches = re.findall(pattern, question, flags=re.IGNORECASE)

    page_numbers = []
    for match in matches:
        if '-' in match:
            start, end = re.findall(r'\d+', match)
            page_numbers.extend(range(int(start), int(end) + 1))
        else:
            parts = re.split(r',|and', match)
            page_numbers.extend([int(part.strip()) for part in parts if part.strip().isdigit()])

    logger.debug(f"Extracted page numbers from question: {page_numbers}")
    return page_numbers