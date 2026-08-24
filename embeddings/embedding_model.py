from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embeddings(chunks):
    """
    Generate embeddings for document chunks.
    """

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(texts)

    for chunk, embedding in zip(chunks, embeddings):
        chunk["embedding"] = embedding.tolist()

    return chunks


def generate_query_embedding(query):
    """
    Generate an embedding for a user query.
    """

    embedding = model.encode(query)

    return embedding.tolist()