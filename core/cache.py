import hashlib

def generate_cache_key(prompt: str) -> str:
    return hashlib.sha256(prompt.encode()).hexdigest()
