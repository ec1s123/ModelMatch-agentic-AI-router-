# scoring.py
import random
from settings import ALPHA, BETA, GAMMA, DELTA
from metrics import load_metrics, dynamic_adjustment

# Models included in routing
MODELS = ["you-pro", "gpt-4-mini", "claude-haiku", "gemini-flash", "mistral-small", "xai-grok4"]

# Priors (task-fit) — heuristic starting points; adapted by metrics over time
PRIORS = {
    "code": {
        "you-pro": 0.80, "gpt-4-mini": 0.77, "claude-haiku": 0.70,
        "gemini-flash": 0.72, "mistral-small": 0.74, "xai-grok4": 0.73
    },
    "reasoning": {
        "gpt-4-mini": 0.85, "you-pro": 0.80, "xai-grok4": 0.82,
        "gemini-flash": 0.76, "mistral-small": 0.78, "claude-haiku": 0.74
    },
    "summarization": {
        "you-pro": 0.81, "gpt-4-mini": 0.76, "claude-haiku": 0.74,
        "gemini-flash": 0.78, "mistral-small": 0.73, "xai-grok4": 0.75
    },
    "search-heavy": {
        "claude-haiku": 0.80, "gemini-flash": 0.77, "you-pro": 0.76,
        "gpt-4-mini": 0.73, "mistral-small": 0.71, "xai-grok4": 0.74
    },
    "general": {
        "you-pro": 0.78, "gpt-4-mini": 0.75, "claude-haiku": 0.74,
        "gemini-flash": 0.76, "mistral-small": 0.73, "xai-grok4": 0.75
    },
}

# Baseline cost/latency priors (lower is better). Refine via metrics at runtime.
COST = {
    "you-pro": 0.22, "gpt-4-mini": 0.30, "claude-haiku": 0.18,
    "gemini-flash": 0.20, "mistral-small": 0.12, "xai-grok4": 0.35
}
LAT = {
    "you-pro": 0.75, "gpt-4-mini": 0.80, "claude-haiku": 0.78,
    "gemini-flash": 0.77, "mistral-small": 0.70, "xai-grok4": 0.85
}

def evidence_boost(task_type: str, search_payload: dict) -> dict:
    # Robustly pull top few titles/snippets
    try:
        results = search_payload.get("results", [])
        if isinstance(results, dict): results = list(results.values())
        elif not isinstance(results, list): results = []
    except Exception:
        results = []
    text = " ".join([(i.get("title","")+" "+i.get("snippet","")) for i in results[:5] if isinstance(i, dict)]).lower()

    boost = {m: 0.0 for m in PRIORS[task_type]}
    if any(k in text for k in ["benchmark", "leaderboard", "comparison"]):
        for m in boost: boost[m] += 0.05
    if task_type == "code" and "code" in text:
        boost["you-pro"] += 0.04; boost["mistral-small"] += 0.02
    if task_type == "reasoning" and any(k in text for k in ["reason", "logic", "math"]):
        boost["gpt-4-mini"] += 0.04; boost["xai-grok4"] += 0.03; boost["gemini-flash"] += 0.02
    if task_type == "search-heavy" and any(k in text for k in ["search", "sources", "web"]):
        boost["claude-haiku"] += 0.04; boost["gemini-flash"] += 0.02
    return boost

def rank_models(task_type: str, search_payload: dict, epsilon: float = 0.03):
    pri = PRIORS[task_type]
    evb = evidence_boost(task_type, search_payload)
    metrics = load_metrics()
    dyn = {m: dynamic_adjustment(m, metrics) for m in pri.keys()}

    scored = []
    for m in pri:
        score = (
            (ALPHA * pri[m]) +
            (BETA  * (1.0 - COST[m])) +
            (GAMMA * (1.0 - LAT[m])) +
            (DELTA * evb[m]) +
            dyn[m]  # learned adjustments from metrics
        )
        scored.append({"model": m, "score": round(score, 4)})

    ranked = sorted(scored, key=lambda x: x["score"], reverse=True)
    # epsilon-greedy exploration (helps learning, adds variety)
    if len(ranked) > 1 and random.random() < epsilon:
        ranked[0], ranked[1] = ranked[1], ranked[0]
    return ranked
