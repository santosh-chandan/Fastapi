from sentence_transformers import SentenceTransformer


# Load ONCE (important)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_text(text: str) -> list[float]:
    # Convert text to vector embedding using HuggingFace.
    # CPU friendly, no API calls.
    model.encode(text, normalize_embeddings=True)

# Why sync, not async?
# HF model runs locally
# No I/O
# Async gives no benefit here
# Do NOT wrap this in async
