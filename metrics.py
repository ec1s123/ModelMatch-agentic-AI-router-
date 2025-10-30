# metrics.py
import json, os, math, threading
from typing import Dict

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
METRICS_PATH = os.path.join(DATA_DIR, "metrics.json")
_lock = threading.Lock()

DEFAULTS = {
    "you-pro":       {"wins": 0, "losses": 0, "thumbs": 0, "avg_latency_ms": 900.0, "avg_cost": 0.0020},
    "gpt-4-mini":    {"wins": 0, "losses": 0, "thumbs": 0, "avg_latency_ms": 950.0, "avg_cost": 0.0030},
    "claude-haiku":  {"wins": 0, "losses": 0, "thumbs": 0, "avg_latency_ms": 980.0, "avg_cost": 0.0018},
    "gemini-flash":  {"wins": 0, "losses": 0, "thumbs": 0, "avg_latency_ms": 960.0, "avg_cost": 0.0020},
    "mistral-small": {"wins": 0, "losses": 0, "thumbs": 0, "avg_latency_ms": 880.0, "avg_cost": 0.0010},
    "xai-grok4":     {"wins": 0, "losses": 0, "thumbs": 0, "avg_latency_ms": 1050.0,"avg_cost": 0.0035},
}

def _read() -> Dict:
    if not os.path.exists(METRICS_PATH):
        return DEFAULTS.copy()
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            # fill any missing keys (new models, etc.)
            for k, v in DEFAULTS.items():
                data.setdefault(k, v.copy())
            return data
        except Exception:
            return DEFAULTS.copy()

def load_metrics() -> Dict:
    with _lock:
        return _read()

def save_metrics(data: Dict):
    with _lock:
        with open(METRICS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

def record_selection(model: str, latency_ms: int, cost_est: float):
    data = load_metrics()
    m = data.get(model, DEFAULTS.get(model, {}).copy())
    alpha = 0.2  # EMA weight
    m["avg_latency_ms"] = (1 - alpha) * m["avg_latency_ms"] + alpha * float(latency_ms)
    m["avg_cost"]       = (1 - alpha) * m["avg_cost"] + alpha * float(cost_est)
    data[model] = m
    save_metrics(data)

def record_feedback(model: str, rating: int):
    data = load_metrics()
    m = data.get(model, DEFAULTS.get(model, {}).copy())
    if rating > 0: m["wins"] += 1
    if rating < 0: m["losses"] += 1
    m["thumbs"] += rating
    data[model] = m
    save_metrics(data)

def dynamic_adjustment(model: str, metrics: Dict) -> float:
    """Small additive boost/penalty from success, latency, cost, sentiment."""
    m = metrics.get(model, DEFAULTS.get(model, {}))
    wins = m.get("wins", 0); losses = m.get("losses", 0)
    wr = wins / max(1, (wins + losses))  # 0..1
    win_component = 0.10 * (wr - 0.5)  # -0.05..+0.05

    lat_list  = [max(1.0, v.get("avg_latency_ms", 900.0)) for v in metrics.values()]
    cost_list = [max(1e-6, v.get("avg_cost", 0.002)) for v in metrics.values()]
    lat_norm  = m.get("avg_latency_ms", 900.0) / max(lat_list)
    cost_norm = m.get("avg_cost", 0.002) / max(cost_list)

    lat_component  = -0.04 * (lat_norm - 1.0)   # slower than fastest → negative
    cost_component = -0.06 * (cost_norm - 1.0)  # pricier than cheapest → negative

    thumbs = m.get("thumbs", 0)
    sentiment_component = 0.04 * math.tanh(thumbs / 10.0)

    return round(win_component + lat_component + cost_component + sentiment_component, 6)
