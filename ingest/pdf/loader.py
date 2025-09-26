from pathlib import Path


def load_pdf(path: str) -> dict:
    # Placeholder: in real impl, parse PDF text + layout
    txt = Path(path).read_text(errors="ignore") if path.endswith(".txt") else "PDF bytes"
    return {"raw": txt, "meta": {"path": path}}


