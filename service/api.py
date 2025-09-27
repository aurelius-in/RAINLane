from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from service.schemas import IngestReq, AnswerReq, AnswerCard, GoldSubmit
from service.model_selector import select_model
from service.provenance import notarize
from ingest.pdf.loader import load_pdf
from ingest.chunking.sectioner import to_sections
from ingest.hashing.hasher import hash_doc
from green_lane.rules.router import route as route_lane
from yellow_lane.fallback.answer import answer_yellow
from service.logging_setup import configure_logging

configure_logging()
app = FastAPI(title="RainLane")

# CORS (relaxed defaults; tighten in prod)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB = {"docs": {}, "gold": [], "answers": {}}


@app.post("/v1/ingest")
def ingest(req: IngestReq):
    raw = load_pdf(req.path)
    sections = to_sections(raw)
    doc_hash = hash_doc(raw)
    DB["docs"][doc_hash] = {"sections": sections, "meta": {"path": req.path}}
    return {"doc_hash": doc_hash, "sections": len(sections)}


@app.get("/")
def root():
    return {"name": "RainLane", "docs": "/docs", "health": "/healthz", "ready": "/readyz", "version": "/version"}


@app.post("/v1/answer", response_model=AnswerCard)
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
    DB["answers"][card.id] = card.model_dump()
    return card


@app.get("/v1/provenance/{answer_id}")
def provenance(answer_id: str):
    return DB["answers"].get(answer_id, {})


@app.post("/v1/gold/submit")
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


