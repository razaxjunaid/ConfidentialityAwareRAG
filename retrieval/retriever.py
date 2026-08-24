from embeddings.embedding_model import generate_query_embedding
from vectorstore.chroma_store import search
from auth.rbac import can_access


def retrieve(query, user_role, top_k=4):
    """
    Retrieve relevant documents and return only the documents
    that the user's role is authorized to access.
    """

    # Step 1: Generate embedding for the user's query
    query_embedding = generate_query_embedding(query)

    # Step 2: Search ChromaDB
    results = search(
        query_embedding=query_embedding,
        top_k=top_k
    )

    # Step 3: Handle empty results
    if (
        not results
        or not results.get("documents")
        or not results["documents"][0]
    ):
        return []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    authorized_results = []

    # Step 4: Apply RBAC
    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        classification = metadata.get(
            "classification",
            "public"
        )

        # Check whether this user can access this classification
        if can_access(user_role, classification):

            authorized_results.append({
                "text": document,
                "filename": metadata.get(
                    "filename",
                    "Unknown"
                ),
                "classification": classification,
                "distance": float(distance)
            })

    return authorized_results