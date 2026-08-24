from sentence_transformers import SentenceTransformer


# Load the embedding model only once
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text: str):
    """
    Generate embedding for a single text.
    """
    return model.encode(text).tolist()


def generate_embeddings(chunks):
    """
    Generate embeddings for all chunks.
    """
    for chunk in chunks:
        chunk["embedding"] = generate_embedding(chunk["text"])

    return chunks


if __name__ == "__main__":

    sample = "Artificial Intelligence is transforming enterprises."

    embedding = generate_embedding(sample)

    print(f"Embedding Dimension : {len(embedding)}")

    print("\nFirst 10 values:\n")

    print(embedding[:10])