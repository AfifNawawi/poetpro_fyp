import faiss
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

VECTOR_DIR = r"C:\Users\nawaw\poetpro-backend\data\vector_db_pantun"

class PantunRetriever:
    def __init__(self):
        print("🔍 Loading vector database...")
        self.index = faiss.read_index(f"{VECTOR_DIR}/pantun.index")

        with open(f"{VECTOR_DIR}/pantun_data.pkl", "rb") as f:
            self.pantun_data = pickle.load(f)

        print("🧠 Loading embedding model...")
        self.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    def search(self, query, top_k=5):
        query_vec = self.model.encode([query]).astype("float32")
        D, I = self.index.search(query_vec, top_k)

        results = []
        for idx in I[0]:
            pantun, source = self.pantun_data[idx]
            results.append({
                "pantun": pantun,
                "source": source
            })

        return results
