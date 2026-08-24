from pathlib import Path


def create_metadata(file_path, classification):
    """
    Create metadata for a document.
    """

    path = Path(file_path)

    return {
        "filename": path.name,
        "file_path": str(path),
        "classification": classification,
        "version": 1
    }


if __name__ == "__main__":

    metadata = create_metadata(
        "data/documents/sample.txt",
        "public"
    )

    print(metadata)