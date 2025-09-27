from pathlib import Path
from typing import Dict


def load_pdf(path: str) -> Dict:
    p = Path(path)
    if not p.exists():
        return {"raw": "", "meta": {"path": path, "error": "not_found"}}
    if path.lower().endswith(".pdf"):
        try:
            import pdfplumber  # type: ignore

            text_parts = []
            with pdfplumber.open(path) as pdf:
                for page in pdf.pages:
                    text_parts.append(page.extract_text() or "")
            txt = "\n\n".join(text_parts)
        except Exception as e:  # graceful fallback
            txt = f"PDF parse failed: {e}"
    else:
        txt = p.read_text(errors="ignore")
    return {"raw": txt, "meta": {"path": path}}


