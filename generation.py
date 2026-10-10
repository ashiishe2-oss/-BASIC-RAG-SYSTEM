import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from google import genai

load_dotenv()

_gen_client = None


def _get_gen_client():
    global _gen_client
    if _gen_client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
        _gen_client = genai.Client(api_key=api_key)
    return _gen_client


def build_prompt(retrieved_chunks, question):
    """
    Augmentation Step:
    Extracts text from retrieved (score, chunk) tuples, joins them with
    blank lines (with page metadata), and wraps them into a grounded
    prompt for the LLM.
    """
    # Step 1: Build labelled context blocks from chunk dicts
    context_blocks = []
    for score, chunk in retrieved_chunks:
        pages_label = ", ".join(str(p) for p in chunk["pages"])
        block = f"[Pages {pages_label}]\n{chunk['text']}"
        context_blocks.append(block)

    # Step 2: Separate each block with a blank line
    context = "\n\n".join(context_blocks)

    # Step 3: Create the augmented prompt with strict instructions
    prompt = f"""You are a helpful assistant. Use only the provided context to answer the question. If the answer cannot be found in the context, say "I do not know based on the provided document."

Context:
{context}

Question: {question}
Answer:"""

    return prompt


def generate_answer(prompt):
    """
    Generation Step:
    Sends the augmented prompt to Gemini and returns the generated answer.
    """
    client = _get_gen_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text
