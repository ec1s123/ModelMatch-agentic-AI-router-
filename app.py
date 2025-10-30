from fastapi import FastAPI
from pydantic import BaseModel
from classifier import classify_task
from providers.you_search import you_search
from scoring import rank_models, COST
from router import run_with_model
import time, json, os
from datetime import datetime, timezone
from fastapi.middleware.cors import CORSMiddleware
from metrics import record_selection, record_feedback, load_metrics

app = FastAPI(title="ModelMatch")

# CORS for local demo UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # demo-friendly; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RouteRequest(BaseModel):
    prompt: str
    mode: str | None = "balanced"   # "balanced" | "quality" | "cost"

class RouteResponse(BaseModel):
    task_type: str
    candidates: list
    chosen: str
    output: str
    latency_ms: int
    # mode: str | None = None  # (optional) include if you want to display it

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "events.jsonl")

@app.get("/")
def root():
    return {"ok": True, "msg": "ModelMatch alive"}

@app.post("/route", response_model=RouteResponse)
def route(req: RouteRequest):
    task = classify_task(req.prompt)
    query = f"best llm for {task['task_type']} tasks benchmark 2025"
    search_payload = you_search(query)

    # ← pass mode through to ranking
    ranked = rank_models(task["task_type"], search_payload, mode=req.mode or "balanced")
    chosen = ranked[0]["model"]

    t0 = time.time()
    output = run_with_model(chosen, req.prompt)
    latency_ms = int((time.time() - t0)*1000)

    cost_est = COST.get(chosen, 0.0015)
    record_selection(chosen, latency_ms, cost_est)

    return RouteResponse(
        task_type=task["task_type"],
        candidates=ranked,
        chosen=chosen,
        output=output,
        latency_ms=latency_ms,
        # mode=req.mode  # (optional)
    )

class Feedback(BaseModel):
    chosen: str
    rating: int   # +1 or -1
    note: str | None = None

@app.post("/feedback")
def feedback(fb: Feedback):
    record_feedback(fb.chosen, fb.rating)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(),
                            "feedback": fb.dict()}) + "\n")
    return {"ok": True}

@app.get("/metrics")
def metrics_view():
    return load_metrics()
