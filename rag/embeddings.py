import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

df = pd.read_csv("catalog/shl_catalog.csv")

# Clean list-like columns
df["job_levels"] = df["job_levels"].astype(str).str.replace(r"[\[\]']", "", regex=True)
df["languages"] = df["languages"].astype(str).str.replace(r"[\[\]']", "", regex=True)
df["keys"] = df["keys"].astype(str).str.replace(r"[\[\]']", "", regex=True)

df["text"] = (
    df["name"].fillna("")
    + ". "
    + df["description"].fillna("")
    + ". Job Levels: "
    + df["job_levels"].fillna("")
    + ". Languages: "
    + df["languages"].fillna("")
    + ". Duration: "
    + df["duration"].fillna("")
    + ". Remote Testing: "
    + df["remote"].fillna("")
    + ". Adaptive: "
    + df["adaptive"].fillna("")
    + ". Status: "
    + df["status"].fillna("")
    + ". Keywords: "
    + df["keys"].fillna("")
)


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings...")

embeddings = model.encode(
    df["text"].tolist(),
    show_progress_bar=True,
    convert_to_numpy=True
)

print("Embedding shape:", embeddings.shape)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings.astype(np.float32))

# Save index
faiss.write_index(index, "catalog/shl_index.faiss")

# Save metadata
df.to_pickle("catalog/shl_metadata.pkl")

print(f"Saved {index.ntotal} embeddings!")