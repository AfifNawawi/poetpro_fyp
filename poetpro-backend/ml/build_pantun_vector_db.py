import pandas as pd
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# ===========================
# Paths
# ===========================
MALAY_FILE = r"C:\Users\nawaw\poetpro-backend\data\cleaned\pantun_malaysia.csv"
SAMPIRAN_FILE = r"C:\Users\nawaw\poetpro-backend\data\cleaned\sampiran_clean.csv"

VECTOR_DIR = r"C:\Users\nawaw\poetpro-backend\data\vector_db_pantun"
os.makedirs(VECTOR_DIR, exist_ok=True)

# ===========================
# Load datasets
# ===========================
print("📥 Loading pantun datasets...")

df_malay = pd.read_csv(MALAY_FILE)
df_sampiran = pd.read_csv(SAMPIRAN_FILE)

pantun_malay = df_malay["pantun"].astype(str).tolist()
pantun_sampiran = df_sampiran["pantun"].astype(str).tolist()

pantuns = pantun_malay + pantun_sampiran

sources = (
    ["MalayCivilization"] * len(pantun_malay) +
    ["Sampiran"] * len(pantun_sampiran)
)

print(f"Total pantun loaded: {len(pantuns)}")

# ===========================
# Load embedding model
# ===========================
print("🧠 Loading embedding model...")
model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

# ===========================
# Generate embeddings
# ===========================
print("🔢 Generating embeddings...")
embeddings = model.encode(pantuns, show_progress_bar=True)

embeddings = np.array(embeddings).astype("float32")

# ===========================
# Build FAISS index
# ===========================
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# ===========================
# Save DB
# ===========================
faiss.write_index(index, os.path.join(VECTOR_DIR, "pantun.index"))

with open(os.path.join(VECTOR_DIR, "pantun_data.pkl"), "wb") as f:
    pickle.dump(list(zip(pantuns, sources)), f)

print("\n✅ Pantun Vector DB built successfully!")
print("Saved at:", VECTOR_DIR)
