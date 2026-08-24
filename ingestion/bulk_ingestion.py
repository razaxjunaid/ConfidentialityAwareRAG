from pathlib import Path

from ingestion.pipeline import process_document
from vectorstore.chroma_store import add_chunks


DOCUMENTS_PATH = Path("data/documents")


def ingest_all_documents():
    """
    Read and ingest all supported documents from the
    classification folders.
    """

    classifications = [
        "public",
        "internal",
        "confidential",
        "highly_confidential"
    ]

    total_chunks = 0

    print("\n========== BULK DOCUMENT INGESTION ==========\n")

    for classification in classifications:

        folder_path = DOCUMENTS_PATH / classification

        if not folder_path.exists():
            print(f"Folder not found: {folder_path}")
            continue

        print(f"\nProcessing classification: {classification}")
        print("-" * 50)

        # Currently process text files
        files = list(folder_path.glob("*.txt"))

        if not files:
            print("No .txt files found.")
            continue

        for file_path in files:

            print(f"\nProcessing: {file_path.name}")

            metadata, chunks = process_document(
                file_path=str(file_path),
                classification=classification,
                chunk_size=50,
                overlap=10
            )

            add_chunks(chunks)

            total_chunks += len(chunks)

            print(f"Chunks created: {len(chunks)}")

    print("\n" + "=" * 50)
    print(f"Total chunks ingested: {total_chunks}")
    print("=" * 50)


if __name__ == "__main__":
    ingest_all_documents()