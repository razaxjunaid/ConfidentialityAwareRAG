from embeddings.embedding_model import generate_query_embedding
from vectorstore.chroma_store import search
from auth.rbac import can_access


def retrieve_with_access_status(query, user_role, top_k=4):
    """
    Retrieve relevant documents and apply RBAC.

    Returns:
    - authorized_results: Documents the user is allowed to access
    - access_denied: True when a restricted document is clearly
      more relevant to the query than accessible documents

    Restricted document content and metadata are NEVER returned
    to the user or the LLM.
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

        distance = float(distance)

        # User is authorized
        if can_access(user_role, classification):

            authorized_results.append({
                "text": document,
                "filename": metadata.get(
                    "filename",
                    "Unknown"
                ),
                "classification": classification,
                "distance": distance
            })

        # User is NOT authorized
        else:
            # Store only the similarity distance.
            # Never expose restricted text or metadata.
            unauthorized_distances.append(distance)

    # Step 5: Determine access status
    access_denied = False

    if unauthorized_distances:

        best_unauthorized_distance = min(
            unauthorized_distances
        )

        # No accessible documents at all
        if not authorized_results:

            access_denied = True

        else:

            best_authorized_distance = min(
                result["distance"]
                for result in authorized_results
            )

            # Smaller distance = more relevant.
            #
            # Use a relevance margin so that a tiny similarity
            # difference does not incorrectly deny access when
            # an authorized document is also relevant.
            RELEVANCE_MARGIN = 0.15

            if (
                best_unauthorized_distance
                + RELEVANCE_MARGIN
                < best_authorized_distance
            ):
                access_denied = True

    return {
        "authorized_results": authorized_results,
        "access_denied": access_denied
    }