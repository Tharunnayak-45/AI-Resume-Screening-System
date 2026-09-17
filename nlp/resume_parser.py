import os


def extract_text(file_path):
    """
    Extract text from PDF or DOCX files.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":

        import PyPDF2

        text = ""

        with open(file_path, "rb") as file:

            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text

    elif extension == ".docx":

        from docx import Document

        document = Document(file_path)

        text = ""

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text

    else:

        return "Unsupported file format."