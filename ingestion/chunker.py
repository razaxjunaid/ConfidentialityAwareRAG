from typing import List, Dict


def split_into_chunks(
    text: str,
    metadata: Dict,
    chunk_size: int = 300,
    overlap: int = 50
) -> List[Dict]:
    """
    Split document text into overlapping chunks while preserving metadata.

    Args:
        text: Document text
        metadata: Document metadata
        chunk_size: Number of words per chunk
        overlap: Number of overlapping words

    Returns:
        List of chunk dictionaries.
    """

    words = text.split()

    chunks = []

    start = 0
    chunk_id = 1

    while start < len(words):

        end = start + chunk_size

        chunk_text = " ".join(words[start:end])

        chunks.append(
            {
                "chunk_id": chunk_id,
                "text": chunk_text,
                "filename": metadata["filename"],
                "file_path": metadata["file_path"],
                "classification": metadata["classification"],
                "version": metadata["version"]
            }
        )

        chunk_id += 1
        start += chunk_size - overlap

    return chunks


if __name__ == "__main__":

    from ingestion.parser import parse_document
    from ingestion.metadata import create_metadata

    file_path = "data/documents/sample.txt"

    # Parse document
    text = parse_document(file_path)

    # Create metadata
    metadata = create_metadata(
        file_path=file_path,
        classification="public"
    )

    # Generate chunks
    chunks = split_into_chunks(
        text=text,
        metadata=metadata,
        chunk_size=5,
        overlap=2
    )

    # Display chunks
    for chunk in chunks:

        print("=" * 60)

        print(f"Chunk ID : {chunk['chunk_id']}")

        print(f"File     : {chunk['filename']}")

        print(f"Class    : {chunk['classification']}")

        print()

        print(chunk["text"])

        print()