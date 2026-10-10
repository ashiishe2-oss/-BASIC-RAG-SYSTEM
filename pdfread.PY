
from pypdf import PdfReader


def read_pdf(path):
    reader = PdfReader(path)

    pages = reader.pages

    content = []

    for pagenum, page in enumerate(pages, start=1):

        text = page.extract_text()

        # Guard: some pages (e.g. image-only or encrypted) return None
        if not text:
            continue

        lines = text.split("\n")
        for line in lines:

            line = line.strip()
            if line:
                content.append((line, pagenum))

    return content
