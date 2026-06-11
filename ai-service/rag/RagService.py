from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model_embed = SentenceTransformer("all-MiniLM-L6-v2")

def search_apps(query, docs, top_k=3):

    doc_embeddings = np.array(model_embed.encode(docs), dtype="float32")

    index = faiss.IndexFlatL2(doc_embeddings.shape[1])
    index.add(doc_embeddings)

    query_embedding = np.array(model_embed.encode([query]), dtype="float32")

    distances, indices = index.search(query_embedding, top_k)

    return [docs[i] for i in indices[0]]