
---

# Insurance Policy Q\&A Assistant (RAG)

This project implements a **Retrieval-Augmented Generation (RAG) system** that allows users to upload **insurance policy PDFs** and ask natural language questions about them. The system processes the documents, stores vector embeddings, and retrieves relevant content to generate accurate answers.

---

## Features

* Upload **PDF documents** (insurance policies).
* Automatic **text extraction, chunking, and embedding**.
* Vector storage in **ChromaDB**.
* Natural language Q\&A powered by **LangChain + LLMs**.
* **Frontend (React)**: clean interface for upload & queries.
* **Backend (FastAPI, Python)**: handles preprocessing and retrieval.

---

## System Architecture

**Flow:**

1. User uploads an insurance policy PDF (frontend).
2. Backend extracts text, chunks it, generates embeddings, and stores them in **ChromaDB**.
3. User submits a question.
4. Backend retrieves relevant chunks and uses a language model via **LangChain** to generate an answer.
5. Frontend displays the answer.

---

## 📂 Project Structure

```
project-root/
├── backend/                 # FastAPI backend
│   ├── api/                 # API routes
│   │   └── main.py
│   │
│   ├── app/                 # Core application logic
│   │   ├── chunker/         # Splits extracted text into chunks
│   │   │   └── chunk.py
│   │   ├── config/          # Configurations and settings
│   │   │   └── settings.py
│   │   ├── embedding/       # Embedding generation
│   │   │   └── embed.py
│   │   ├── llm/             # LLM utilities (retrieval-augmented generation)
│   │   ├── pdf_loader/      # PDF text extraction
│   │   ├── retriever/       # Retrieval logic
│   │   └── utils/           # Helper utilities
│   │
│   ├── data/                # Uploaded PDFs or processed text
│   ├── vectorstores/        # ChromaDB vector storage
│   └── myenv/               # Local Python environment (ignored in Git)
│
├── frontend/                # React frontend
│   ├── src/                 # Components, pages, services
│   └── package.json
│
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack

* **Frontend:** React
* **Backend:** FastAPI, Python
* **Vector DB:** ChromaDB
* **Orchestration:** LangChain
* **PDF Processing:** PyPDFLoader
* **Model Provider:** Ollama

---

## ▶️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/tanishkac/insurance_bot
cd your-repo
```

### 2. Setup Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload
```

### 3. Setup Frontend

```bash
cd frontend
npm install
npm start
```

### 4. Usage

1. Upload an insurance policy PDF from the frontend.
2. Ask natural language questions.
3. Receive context-aware answers.

---

## Future Enhancements

* Multi-PDF support.
* Chat history (conversational context).
* More file format support (Word, Excel).
* Deployment on **Vercel (frontend)** + **Render/Heroku (backend)**.

---

## Conclusion

This project demonstrates how **RAG (Retrieval Augmented Generation)** can make complex insurance policies accessible to users by enabling natural language queries. It integrates **React + FastAPI + LangChain + ChromaDB** to create an end-to-end intelligent assistant.


