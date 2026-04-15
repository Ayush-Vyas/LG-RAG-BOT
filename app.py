import os
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import chromadb
from sentence_transformers import SentenceTransformer

# ---------------- APP ----------------
app = FastAPI(title="LG Manuals AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- LOAD MODEL ----------------
print("Loading embedding model...")
sbert = SentenceTransformer("all-MiniLM-L6-v2")

client_db = chromadb.PersistentClient(path="./chroma_db")
collection = client_db.get_or_create_collection(name="lg_docs")

# ---------------- REQUEST MODEL ----------------
class ChatRequest(BaseModel):
    question: str
    top_k: int = 3

# ---------------- CLEANING FUNCTION ----------------
def format_steps(text: str):
    text = (
        text.replace("•", " ")
            .replace("\n", " ")
            .replace("  ", " ")
            .strip()
    )

    # split into sentence-like chunks
    parts = [p.strip() for p in text.split(".") if p.strip()]

    # fallback if splitting fails
    if len(parts) == 1:
        parts = [text]

    return "\n".join([f"{i+1}. {p}" for i, p in enumerate(parts)])

# ---------------- ROUTES ----------------
@app.get("/")
def home():
    return {"message": "LG Manuals AI API is running 🚀"}

@app.post("/chat")
def chat(req: ChatRequest):
    q = req.question.strip()
    if not q:
        raise HTTPException(status_code=400, detail="Empty question")

    # 1. Embed question
    q_emb = sbert.encode([q], convert_to_numpy=True)

    # 2. Search vector DB
    res = collection.query(
        query_embeddings=q_emb.tolist(),
        n_results=req.top_k
    )

    docs = res.get("documents", [[]])[0]

    if not docs:
        return {"answer": "No relevant info found."}

    # 3. Combine retrieved chunks
    combined_text = " ".join(docs)

    # 4. FORMAT LIKE OLD SYSTEM (IMPORTANT PART)
    answer = format_steps(combined_text)

    return {"answer": answer}