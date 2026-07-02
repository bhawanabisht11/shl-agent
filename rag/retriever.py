import faiss
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import os

print("🚀 retriever started")

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Safe paths
BASE_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(BASE_DIR)

index = faiss.read_index(
    os.path.join(PROJECT_ROOT, "catalog", "shl_index.faiss")
)

df = pd.read_pickle(
    os.path.join(PROJECT_ROOT, "catalog", "shl_metadata.pkl")
)


# -----------------------------
# EMBEDDING FUNCTION
# -----------------------------
def get_query_embedding(query):
    return model.encode([query], convert_to_numpy=True)


# -----------------------------
# MAIN RETRIEVAL FUNCTION
# -----------------------------
def retrieve(query, top_k=10):
    print("\n🔍 Query:", query)

    query_vec = get_query_embedding(query)

    distances, indices = index.search(query_vec.astype(np.float32), top_k)

    if len(indices[0]) == 0:
        return []

    results = df.iloc[indices[0]]

    return results[
        ["name", "description", "job_levels", "languages", "duration"]
    ].to_dict(orient="records")


# -----------------------------
# TEST BLOCK
# -----------------------------
if __name__ == "__main__":
    print("\n🧪 TEST RUN")

    query = "Need Java developer assessment"
    results = retrieve(query)

    print("\n✅ FINAL RESULTS:\n")

    for i, result in enumerate(results, start=1):
        print(f"\n{i}. {result['name']}")
        print(f"Description : {result['description']}")
        print(f"Job Levels  : {result['job_levels']}")
        print(f"Languages   : {result['languages']}")
        print(f"Duration    : {result['duration']}")