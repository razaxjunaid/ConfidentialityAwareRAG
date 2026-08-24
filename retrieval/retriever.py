from embeddings.embedding_model import generate_embedding
from vectorstore.chroma_store import search
from auth.rbac import can_access


def retrieve(query: str, user_role: str, top_k: int = 5):
    """
    Retrieve relevant chunks and filter them
    according to the user's clearance level.
    """

    # Generate embedding for the user's query
    query_embedding = generate_embedding(query)

    # Retrieve more results initially because some
    # results may be removed due to access restrictions
    results = search(
        query_embedding=query_embedding,
        top_k=top_k
    )

    secure_results = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # Check each retrieved document
    for i in range(len(documents)):

        document_classification = metadatas[i]["classification"]

        # Check whether the user can access this document
        if can_access(user_role, document_classification):

            secure_results.append({
                "text": documents[i],
                "filename": metadatas[i]["filename"],
                "classification": document_classification,
                "version": metadatas[i]["version"],
                "distance": distances[i]
            })

    return secure_results


if __name__ == "__main__":

    query = "Tell me about company strategy, financial plans, and sensitive information."

    roles = [
        "viewer",
        "staff",
        "senior",
        "executive"
    ]

    print("\n========== RBAC CONFIDENTIALITY TEST ==========\n")

    print(f"Query: {query}\n")

    for user_role in roles:

        print("\n" + "#" * 60)
        print(f"USER ROLE: {user_role.upper()}")
        print("#" * 60)

        results = retrieve(
            query=query,
            user_role=user_role,
            top_k=4
        )

        if not results:
            print("\nNo authorized documents found.\n")
            continue

        for i, result in enumerate(results, start=1):

            print("\n" + "=" * 60)
            print(f"Rank           : {i}")
            print(f"File           : {result['filename']}")
            print(f"Classification : {result['classification']}")
            print(f"Distance       : {result['distance']:.4f}")

            print("\nContent:")
            print(result["text"])