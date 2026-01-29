import faiss
import pickle
from sentence_transformers import SentenceTransformer

VECTOR_DIR = r"C:\Users\nawaw\poetpro-backend\data\vector_db_syair"

class SyairRetriever:
    def __init__(self):
        self.index = faiss.read_index(f"{VECTOR_DIR}/syair.index")

        with open(f"{VECTOR_DIR}/syair_data.pkl", "rb") as f:
            self.syair_data = pickle.load(f)

        self.model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    def search(self, query, top_k=5):
        query_vec = self.model.encode([query]).astype("float32")
        D, I = self.index.search(query_vec, top_k)

        results = []
        for idx in I[0]:
            results.append(self.syair_data[idx])

        return results
