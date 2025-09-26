from typing import Tuple, Dict
from green-lane.rules.tasks import detect_task


# naive heuristics: treat known certified Qs as green
CERT = {
    "what is the sterile changeover checklist?": {
        "answer": "Use SOP 4.2 steps A–F; verify gauges; record signoff in Form RX-12.",
        "citations": [{"doc_id": "sop-42", "section": "4.2", "span": [10, 120]}],
    }
}


def route(query: str, role: str) -> Tuple[str, Dict]:
    q = query.strip().lower()
    if q in CERT:
        info = CERT[q]
        return "green", {
            "task": detect_task(q),
            "canonical_answer": info["answer"],
            "citations": info["citations"],
        }
    return "yellow", {"task": detect_task(q)}


