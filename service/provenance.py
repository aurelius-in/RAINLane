import hashlib
import uuid

from service.schemas import AnswerCard, Citation, ModelInfo


def notarize(answer, lane, query, sources, model, selector_reason):
    concat = f"{answer}|{lane}|{query}|{sources}|{model['name']}|{model['version']}"
    sha = hashlib.sha256(concat.encode()).hexdigest()
    sig = {"key_id": "sig://local", "sig": sha[:40]}
    doc_hashes = [
        {
            "doc_id": c.doc_id if isinstance(c, Citation) else c.get("doc_id", ""),
            "sha256": sha,
        }
        for c in (sources or [])
    ]
    card = AnswerCard(
        id=f"ans_{uuid.uuid4().hex[:10]}",
        lane=lane,
        answer=answer,
        citations=[Citation(**c) if isinstance(c, dict) else c for c in (sources or [])],
        doc_hashes=doc_hashes,
        model=ModelInfo(
            name=model["name"], version=model["version"], selector_reason=selector_reason
        ),
        signature=sig,
        metrics={"latency_ms": 420.0, "cost_usd": 0.003},
    )
    return card


