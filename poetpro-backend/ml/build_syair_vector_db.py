import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

DATA_FILE = r"C:\Users\nawaw\poetpro-backend\data\cleaned\syair_clean.txt"
VECTOR_DIR = r"C:\Users\nawaw\poetpro-backend\data\vector_db_syair"

os.makedirs(VECTOR_DIR, exist_ok=True)

with open(DATA_FILE, "r", encoding="utf-8") as f:
    text = f.read()

syairs = [s.strip() for s in text.split("\n\n") if len(s.strip()) > 20]

print("Total syairs:", len(syairs))

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
embeddings = model.encode(syairs, show_progress_bar=True).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, f"{VECTOR_DIR}/syair.index")

with open(f"{VECTOR_DIR}/syair_data.pkl", "wb") as f:
    pickle.dump(syairs, f)

print("✅ Syair vector DB built successfully")
