# pyrefly: ignore [missing-import]
from pdfread import read_pdf

# pyrefly: ignore [missing-import]
from chunker import create_chunks
from embeddings import get_embeddings
from similarity import find_similar_chunks
from generation import build_prompt, generate_answer

# ── Step 1: Extract text from the PDF ──────────────────────────────────────
content = read_pdf("test1.pdf")

# ── Step 2: Split into overlapping chunks ──────────────────────────────────
chunks = create_chunks(content)

# ── Step 3: Embed each chunk's text (keep full chunk dict separate) ─────────
vectors = []
for chunk in chunks:
    vectors.append(get_embeddings(chunk["text"]))

# ── Step 4: Ask the user a question and embed it ───────────────────────────
question = input("Ask a question: ")
query_vector = get_embeddings(question)

# ── Step 5: Find the most similar chunks ────────────────────────────────────
results = find_similar_chunks(query_vector, vectors, chunks)

# ── Step 6: Print retrieved chunks ──────────────────────────────────────────
if not results:
    print("\nNo relevant information found in the document for that question.")
else:
    for i, (score, chunk) in enumerate(results):
        print(f"\nResult {i + 1}")
        print(f"Similarity: {score:.4f}")
        print(f"Text: {chunk['text']}")
        print(f"Pages: {chunk['pages']}")

    # ── Step 7: Build the augmented prompt ──────────────────────────────────
    augmented_prompt = build_prompt(results, question)
    source_pages = results[0][1]["pages"]

    print("\n=== AUGMENTED PROMPT ===")
    print(augmented_prompt)

    # ── Step 8: Generate and print the answer ───────────────────────────────
    answer = generate_answer(augmented_prompt)

    print("\n=== ANSWER ===")
    print(answer)
    print(f"Source Pages: {source_pages}")
