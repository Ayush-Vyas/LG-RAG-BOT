# 🤖 LG RAG BOT (Retrieval-Augmented Generation System)

A smart AI-powered chatbot that allows users to ask questions about LG appliance manuals and get accurate, step-by-step answers using semantic search and AI.

This project uses a full **RAG (Retrieval-Augmented Generation)** pipeline with FastAPI backend and React frontend.

---

## 🚀 Features

- 🔍 Semantic search over LG appliance manuals (PDFs)
- 🧠 AI-powered contextual answers using retrieved documents
- 📄 Supports multiple appliance manuals (washing machine, etc.)
- ⚡ Fast vector search using ChromaDB
- 💬 Chat-based interactive UI (React frontend)
- 📚 Clean step-by-step response formatting
- 🔗 FastAPI backend integration
- 🧩 Complete RAG pipeline implementation

---

## 🧰 Tech Stack

**Frontend:**
- React (Vite)
- JavaScript (JSX)
- CSS

**Backend:**
- Python
- FastAPI
- SentenceTransformers (`all-MiniLM-L6-v2`)
- ChromaDB

**AI / NLP:**
- Embeddings-based semantic search
- Retrieval-Augmented Generation (RAG)

---

## 📁 Project Structure


```
LG-RAG-BOT/
│
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
│
├── app.py                   # FastAPI backend
├── main.py                  # Utility file
├── manuals/                 # PDF manuals dataset
├── chroma_db/               # Vector DB (ignored in Git)
│
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/LG-RAG-BOT.git
cd LG-RAG-BOT

---

### 2️⃣ Backend Setup
```bash
pip install fastapi uvicorn chromadb sentence-transformers
```

Run backend:
```bash
uvicorn app:app --reload
```

---

### 3️⃣ Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🧠 How It Works

1. User asks a question  
2. Query converted into embeddings  
3. ChromaDB retrieves relevant manual chunks  
4. Backend formats response  
5. User gets clean step-by-step answer  

---

## 💡 Example Questions

- How to clean washing machine filter?
- Why is machine not draining water?
- What does OE error mean?
- How to fix vibration issue?
- How to run cleaning cycle?

---

## ⚠️ Notes

- `chroma_db/` is ignored (local DB)
- `manuals/` contains PDF dataset
- Backend must run before frontend

---

## 👨‍💻 Author

Aarchi Patel
Ayush Vyas

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!
