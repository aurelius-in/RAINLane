from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from service.schemas import IngestReq, AnswerReq, AnswerCard, GoldSubmit
from service.model_selector import select_model
from service.provenance import notarize
from ingest.pdf.loader import load_pdf
from ingest.chunking.sectioner import to_sections
from ingest.hashing.hasher import hash_doc
from service.db import SessionLocal, engine
from service.models import Base, Document, Section, Answer as AnswerModel
from green_lane.rules.router import route as route_lane
from yellow_lane.fallback.answer import answer_yellow
from service.logging_setup import configure_logging
from service.auth import require_api_key
from service.rate_limit import limit_requests
from service.otel import init_otel

configure_logging()
init_otel()
app = FastAPI(title="RainLane")
Base.metadata.create_all(bind=engine)

# CORS (relaxed defaults; tighten in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = {"docs": {}, "gold": []}


@app.post("/v1/ingest", dependencies=[Depends(require_api_key), Depends(limit_requests)])
def ingest(req: IngestReq):
    raw = load_pdf(req.path)
    sections = to_sections(raw)
    doc_hash = hash_doc(raw)
    DB["docs"][doc_hash] = {"sections": sections, "meta": {"path": req.path}}
    with SessionLocal() as s:
        s.merge(Document(doc_hash=doc_hash, path=req.path, meta=raw.get("meta", {})))
        for sec in sections:
            s.add(Section(doc_hash=doc_hash, section_id=sec.get("id",""), title=sec.get("title",""), text=sec.get("text","")))
        s.commit()
    return {"doc_hash": doc_hash, "sections": len(sections)}


@app.get("/")
def root():
    return {"name": "RainLane", "docs": "/docs", "health": "/healthz", "ready": "/readyz", "version": "/version"}


@app.post("/v1/answer", response_model=AnswerCard, dependencies=[Depends(require_api_key), Depends(limit_requests)])
def answer(req: AnswerReq):
    lane, policy_info = route_lane(req.query, req.user_role)
    task = policy_info.get("task", "extractive")
    model, selector_reason = select_model(task, req.query, lane)
    if lane == "green":
        ans = policy_info.get("canonical_answer", "")
        if not ans:
            raise HTTPException(400, "No certified coverage for this query")
        card = notarize(
            ans,
            lane,
            req.query,
            sources=policy_info.get("citations", []),
            model=model,
            selector_reason=selector_reason,
        )
    else:
        ans, citations = answer_yellow(req.query, DB["docs"])
        card = notarize(
            ans,
            lane,
            req.query,
            sources=citations,
            model=model,
            selector_reason=selector_reason,
        )
    with SessionLocal() as s:
        s.add(AnswerModel(
            id=card.id,
            lane=card.lane,
            answer=card.answer,
            citations=[c.model_dump() for c in card.citations],
            doc_hashes=card.doc_hashes,
            model=card.model.model_dump(),
            signature=card.signature,
            metrics=card.metrics,
        ))
        s.commit()
    return card


@app.get("/v1/provenance/{answer_id}")
def provenance(answer_id: str):
    with SessionLocal() as s:
        row = s.get(AnswerModel, answer_id)
        return row.__dict__ if row else {}


@app.post("/v1/gold/submit", dependencies=[Depends(require_api_key)])
def gold_submit(req: GoldSubmit):
    DB["gold"].append(req.model_dump())
    return {"ok": True, "count": len(DB["gold"]) }


@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/readyz")
def readyz():
    # Basic readiness: app started
    return {"ready": True}


try:
    from pathlib import Path

    VERSION = (Path(__file__).resolve().parents[1] / "VERSION").read_text().strip()
except Exception:
    VERSION = "0.0.0"


@app.get("/version")
def version():
    return {"version": VERSION}


