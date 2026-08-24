import chromadb


# -----------------------------------------------------
# Create Persistent Chroma Client
# -----------------------------------------------------

client = chromadb.PersistentClient(
    path="data/chroma_db"
)


# Create (or load) collection
collection = client.get_or_create_collection(
    name="enterprise_documents"
)


# -----------------------------------------------------
# Store Chunks
# -----------------------------------------------------

def add_chunks(chunks):
    """
    Store chunks and their embeddings in ChromaDB.
    """

    # Do not send an empty list to ChromaDB
    if not chunks:
        print("⚠️ No chunks to store.")
        return

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for chunk in chunks:

        # Unique ID based on classification, filename,
        # and chunk ID
        chunk_id = (
            f"{chunk['classification']}_"
            f"{chunk['filename']}_"
            f"{chunk['chunk_id']}"
        )

        ids.append(chunk_id)

        documents.append(
            chunk["text"]
        )

        embeddings.append(
            chunk["embedding"]
        )

        metadatas.append(
            {
                "filename": chunk["filename"],
                "classification": chunk["classification"],
                "version": chunk["version"]
            }
        )

    try:

        # Upsert prevents duplicate-ID errors
        collection.upsert(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(
            f"\n✅ {len(chunks)} chunks stored successfully.\n"
        )

    except Exception as e:

        print("\n❌ Error storing chunks.\n")
        print(e)


# -----------------------------------------------------
# Semantic Search
# -----------------------------------------------------

def search(query_embedding, top_k=5):
    """
    Search similar chunks.
    """

    # Check how many documents exist
    total_documents = collection.count()

    if total_documents == 0:
        return None

    # ChromaDB cannot return more documents
    # than actually exist
    n_results = min(top_k, total_documents)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results


# -----------------------------------------------------
# Show Collection Info
# -----------------------------------------------------

def collection_info():
    """
    Print collection statistics.
    """

    print("\n========== CHROMADB ==========\n")

    print(
        "Collection Name :",
        collection.name
    )

    print(
        "Total Documents :",
        collection.count()
    )


# -----------------------------------------------------
# Delete Everything
# -----------------------------------------------------

def clear_collection():
    """
    Delete all vectors from the collection.
    """

    global collection

    client.delete_collection(
        "enterprise_documents"
    )

    collection = client.get_or_create_collection(
        name="enterprise_documents"
    )

    print("\n🗑️ Collection cleared.\n")


# -----------------------------------------------------
# Testing
# -----------------------------------------------------

if __name__ == "__main__":

    # clear_collection()

    collection_info()


def debug_collection():
    """
    Print all documents and metadata stored in ChromaDB.
    """
    results = collection.get(
        include=["documents", "metadatas"]
    )

    print("\n========== STORED DOCUMENTS ==========\n")

    for i, (document, metadata) in enumerate(
        zip(results["documents"], results["metadatas"]),
        start=1
    ):
        print(f"Document {i}")
        print("Metadata:", metadata)
        print("Text:", document[:200])
        print("-" * 50)