import os
import pdfplumber
import chromadb
from sentence_transformers import SentenceTransformer

# ---------- SETTINGS ----------
folder_path = "manuals"
chroma_path = "./chroma_db"
collection_name = "lg_docs"

# ---------- HELPER FUNCTIONS ----------
def extract_text_from_pdf(pdf_path):
    all_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                all_text.append(text.strip())
    return "\n".join(all_text)

def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# ---------- LOAD MODEL ----------
print("🔄 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ---------- INIT CHROMA ----------
client = chromadb.PersistentClient(path=chroma_path)
collection = client.get_or_create_collection(name=collection_name)

# ---------- LOAD DATA IF EMPTY ----------
if collection.count() == 0:
    print("⚡ No data in DB. Processing PDFs...")
    doc_count = 0

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            print(f"📄 Processing {filename}...")

            text = extract_text_from_pdf(pdf_path)
            chunks = chunk_text(text)

            embeddings = model.encode(chunks, convert_to_numpy=True, show_progress_bar=True)

            collection.add(
                documents=chunks,
                embeddings=[e.tolist() for e in embeddings],
                ids=[f"{filename}_{i}" for i in range(len(chunks))]
            )

            doc_count += len(chunks)

    print(f"✅ Inserted {doc_count} chunks into ChromaDB")
else:
    print("✅ ChromaDB already contains data")