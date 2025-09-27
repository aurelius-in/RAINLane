from typing import Dict, List, Tuple


def _score(text: str, query: str) -> int:
    q = query.lower().split()
    t = text.lower()
    return sum(1 for w in q if w in t)


def answer_yellow(query: str, docs: Dict[str, Dict]) -> Tuple[str, List[Dict]]:
    best = (0, None, None)  # score, doc_hash, section
    for doc_hash, rec in docs.items():
        for sec in rec.get("sections", []):
            s = _score(sec.get("text", ""), query)
            if s > best[0]:
                best = (s, doc_hash, sec)
    if best[1] is None:
        return f"Advisory: No matching section found for '{query}'.", []
    sec = best[2]
    citations = [
        {
            "doc_id": best[1],
            "section": sec.get("id", ""),
            "span": [0, min(50, len(sec.get("text", "")))],
        }
    ]
    snippet = sec.get("text", "")[:200]
    return f"Advisory: {snippet}", citations
