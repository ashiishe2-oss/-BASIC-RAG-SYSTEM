# pyrefly: ignore [missing-import]
import numpy as np


def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)

    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    similarity = dot_product / (magnitude_a * magnitude_b)

    return float(similarity)


def find_similar_chunks(query_vector, vectors, chunks):
    scores = []

    # Calculate similarity between the question and every chunk
    for i in range(len(vectors)):
        score = cosine_similarity(query_vector, vectors[i])
        scores.append((score, chunks[i]))

    # Highest similarity first
    scores.sort(key=lambda x: x[0], reverse=True)

    best = scores[0][0]
    all_scores = [s for s, _chunk in scores]
    avg = sum(all_scores) / len(all_scores)
    diff = best - avg

    print(f"[Similarity] best={best:.4f}  avg={avg:.4f}  diff={diff:.4f}")

    # Reject if: the top score is too low (no chunk is truly relevant)
    # OR the best score barely stands out from the rest (query is off-topic)
    if best < 0.5 or diff < 0.1:
        print("No sufficiently relevant chunks found.")
        return []

    # Select up to 3 unique, non-redundant chunks
    top3 = []
    seen_texts = set()

    for score, chunk in scores:
        text = chunk["text"]

        if text not in seen_texts:
            top3.append((score, chunk))
            seen_texts.add(text)

        if len(top3) == 3:
            break

    return top3