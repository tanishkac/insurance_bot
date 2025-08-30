from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from app.pdf_loader.extract import load_pdf
from app.chunker.chunk import chunk_documents
from app.embedding.embed import get_embedding_function, create_vectorstore, delete_vectorstore, load_vectorstore
from app.utils.chunk_io import save_chunks, load_chunks
from app.llm.llm_provider import get_llm_instance
from app.llm.generator import generate_answer
import uuid
import tempfile
from fastapi import UploadFile
import os

app = FastAPI()

class ChatRequest(BaseModel):
    document_id: str
    message: str

@app.get("/")
async def root():
    return {"message": "API is running."}

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    tmp_path = None
    try:
        # Generate a unique document ID
        document_id = str(uuid.uuid4())

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        
        # Call existing load_pdf with file path
        pages = load_pdf(tmp_path)
        
        # Proceed with chunking and embedding as usual
        chunks = chunk_documents(pages)
        embedding_function = get_embedding_function()
        vectorstore_path = f"./vectorstores/{document_id}"

        if not os.path.exists(vectorstore_path):
            os.makedirs(vectorstore_path)

        save_chunks(chunks, os.path.join(vectorstore_path, "chunks.json"))
        create_vectorstore(chunks, embedding_function, vectorstore_path)

        return {"message": "PDF uploaded and indexed successfully", "document_id": document_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        # Remove temporary file safely
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.post("/chat")
async def chat(request: ChatRequest):
   
    try:
        vectorstore_path = f"./vectorstores/{request.document_id}"
        # Load stored data for this user
        vectorstore = load_vectorstore(vectorstore_path)
        all_chunks = load_chunks(os.path.join(vectorstore_path, "chunks.json"))
        llm = get_llm_instance()
        answer = generate_answer(request.message, all_chunks, vectorstore, llm)
        return {"response": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/end_session")
async def end_session(document_id: str):
    try:
        vectorstore_path = f"./vectorstores/{document_id}"
        delete_vectorstore(vectorstore_path)
        return {"message": "Session cleaned up."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
