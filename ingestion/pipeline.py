from ingestion.parser import parse_document
from ingestion.metadata import create_metadata
from ingestion.chunker import split_into_chunks
from embeddings.embedding_model import generate_embeddings


def process_document(file_path: str,
                     classification: str,
                     chunk_size: int = 300,
                     overlap: int = 50):
    """
    Complete ingestion pipeline.

    Returns
    -------
    metadata
    chunks
    """

    print("\n========== DOCUMENT INGESTION ==========\n")

    # Step 1
    print("Parsing document...")
    text = parse_document(file_path)

    # Step 2
    print("Creating metadata...")
    metadata = create_metadata(
        file_path=file_path,
        classification=classification
    )

    # Step 3
    print("Generating chunks...")
    chunks = split_into_chunks(
        text=text,
        metadata=metadata,
        chunk_size=chunk_size,
        overlap=overlap
    )

    print("Generating embeddings...")

    chunks = generate_embeddings(chunks)

    print(f"\nTotal Chunks Created : {len(chunks)}")

    return metadata, chunks

if __name__ == "__main__":

    metadata, chunks = process_document(
        file_path="data/documents/sample.txt",
        classification="public",
        chunk_size=5,
        overlap=2
    )

    print("\nMetadata\n")
    print(metadata)

    print("\nChunks\n")

    for chunk in chunks:

        print("=" * 60)

        print(chunk)