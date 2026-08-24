from embeddings.embedding_model import generate_query_embedding
from vectorstore.chroma_store import search
from auth.rbac import can_access


def retrieve_with_access_status(query, user_role, top_k=4):
    """
    Retrieve relevant documents and separate them into:

    1. Authorized documents
    2. Unauthorized documents

    Unauthorized document content is NEVER returned to the LLM.
    """

    # Step 1: Generate query embedding
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
        return {
            "authorized_results": [],
            "access_denied": False
        }

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    authorized_results = []
    unauthorized_distances = []

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

        # User has permission
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

        # User does NOT have permission
        else:
            # Only store distance internally.
            # NEVER return document text or metadata to the user/LLM.
            unauthorized_distances.append(float(distance))

    # Step 5: Detect whether the best matching result was restricted
    access_denied = False

    if unauthorized_distances:

        best_unauthorized_distance = min(unauthorized_distances)

        if not authorized_results:
            access_denied = True

        else:
            best_authorized_distance = min(
                result["distance"]
                for result in authorized_results
            )

            # Smaller distance = more relevant
            if best_unauthorized_distance < best_authorized_distance:
                access_denied = True

    return {
        "authorized_results": authorized_results,
        "access_denied": access_denied
    }