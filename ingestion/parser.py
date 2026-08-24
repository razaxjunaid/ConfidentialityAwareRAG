from pathlib import Path
from pypdf import PdfReader
from docx import Document


def parse_pdf(file_path):
    """
    Extract text from a PDF.
    """

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        extracted = page.extract_text()

        if extracted:
            text += extracted + "\n"

    return text


def parse_docx(file_path):
    """
    Extract text from DOCX.
    """

    document = Document(file_path)

    paragraphs = []

    for para in document.paragraphs:
        paragraphs.append(para.text)

    return "\n".join(paragraphs)


def parse_txt(file_path):
    """
    Extract text from TXT.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def parse_document(file_path):
    """
    Automatically detect file type.
    """

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return parse_pdf(file_path)

    elif extension == ".docx":
        return parse_docx(file_path)

    elif extension == ".txt":
        return parse_txt(file_path)

    else:
        raise ValueError(f"Unsupported file type: {extension}")


if __name__ == "__main__":

    file_path = "data/documents/sample.txt"

    text = parse_document(file_path)

    print(text)