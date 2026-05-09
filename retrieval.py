from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

dimension = 384

stored_chunks = []

index = None


def create_index(chunks):
    global stored_chunks
    global index

    print("Creating embeddings...")
    print(f"Chunks received: {len(chunks)}")

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts)

    embeddings = np.array(embeddings).astype("float32")

    print(f"Embeddings shape: {embeddings.shape}")

    # CREATE NEW INDEX
    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    print(f"FAISS total vectors: {index.ntotal}")

    stored_chunks = chunks

    print(f"Stored chunks: {len(stored_chunks)}")


def search(query, k=3):
    global index

    if index is None:
        return []

    if len(stored_chunks) == 0:
        return []

    print(f"Searching for: {query}")

    query_embedding = model.encode([query])

    query_embedding = np.array(query_embedding).astype("float32")

    distances, indices = index.search(query_embedding, k)

    print("Indices:", indices)

    results = []

    for idx, distance in zip(indices[0], distances[0]):

        if idx == -1:
            continue

        if idx >= len(stored_chunks):
            continue

        result = stored_chunks[idx].copy()

        result["score"] = float(distance)

        results.append(result)

    return results