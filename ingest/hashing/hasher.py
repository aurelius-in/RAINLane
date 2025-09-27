import hashlib


def hash_doc(raw_doc: dict) -> str:
    data = raw_doc.get("raw", "")
    return hashlib.sha256(str(data).encode()).hexdigest()


