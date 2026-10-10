def create_chunks(content):

    chunks = []

    chunk_size = 5
    overlap = 1

    # Create overlapping chunks
    for i in range(0, len(content), chunk_size - overlap):

        chunk = content[i:i + chunk_size]

        text = []
        pages = []

        # Extract text and page number from each item
        for line, page_num in chunk:
            text.append(line)
            pages.append(page_num)

        # Remove duplicate page numbers, keep them sorted
        pages = sorted(set(pages))

        # Store text + page metadata
        chunks.append({
            "text": " ".join(text),
            "pages": pages
        })

    return chunks