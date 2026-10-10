import os
import time
import socket
# pyrefly: ignore [missing-import]
import httpx
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from google import genai
from google.genai import errors

load_dotenv()

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable is not set.")
        _client = genai.Client(api_key=api_key)
    return _client


def get_embeddings(text, max_retries=3, backoff_factor=1.5):
    global _client
    for attempt in range(1, max_retries + 1):
        try:
            client = _get_client()
            result = client.models.embed_content(
                model="gemini-embedding-2",
                contents=text
            )
            return result.embeddings[0].values
        except (httpx.ConnectError, httpx.TimeoutException, httpx.NetworkError, socket.gaierror, errors.APIError) as err:
            _client = None  # Reset client and underlying connection pool on network failure
            if attempt == max_retries:
                raise RuntimeError(
                    f"Gemini API network connection failed after {max_retries} attempts: {err}"
                ) from err
            time.sleep(backoff_factor * attempt)