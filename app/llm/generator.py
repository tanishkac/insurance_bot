# app/llm/generator.py

from langchain_core.prompts import ChatPromptTemplate
from app.retriever.retrieve import get_relevant_chunks
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Prompt template
PROMPT_TEMPLATE = """
You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer
the question. If you don't know the answer, say that you
don't know. DON'T MAKE UP ANYTHING.

{context}

---

Answer the question based on the above context: {question}
"""

prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

def generate_answer(question: str, all_chunks, vectorstore, llm, top_k: int = 5) -> str:
    logger.info(f"Generating answer for question: '{question}'")

    # Step 1: Retrieve relevant chunks (page-aware)
    relevant_chunks = get_relevant_chunks(question, all_chunks, vectorstore, top_k=top_k)

    if not relevant_chunks:
        logger.warning("No relevant chunks found. Returning fallback response.")
        return "I couldn't find relevant information to answer that question."

    # Step 2: Prepare context
    context_text = "\n\n".join(chunk.page_content for chunk in relevant_chunks)
    logger.debug(f"Context text length: {len(context_text)} characters")

    # Step 3: Format prompt
    prompt = prompt_template.format(context=context_text, question=question)
    logger.debug(f"Final prompt sent to LLM:\n{prompt}")

    # Step 4: Invoke LLM
    try:
        response = llm.invoke(prompt)
        logger.info("LLM response generated successfully.")
    except Exception as e:
        logger.exception("Error during LLM invocation")
        return "An error occurred while generating the answer."

    return response
