import re

def classify_task(prompt: str) -> dict:
    p = prompt.lower()
    if any(k in p for k in ["write code", "refactor", "unit test", "python", "bug", "leetcode"]):
        t = "code"
    elif any(k in p for k in ["summarize", "abstract", "tl;dr", "condense"]):
        t = "summarization"
    elif "http" in p or "www." in p or any(k in p for k in ["sources", "citations", "research"]):
        t = "search-heavy"
    elif any(k in p for k in ["why", "prove", "derive", "step by step", "reason"]):
        t = "reasoning"
    else:
        t = "general"

    length = "short" if len(p) < 240 else "long"
    difficulty = "high" if re.search(r"\b(optimize|prove|theorem|multi-step|chain)\b", p) else "normal"
    return {"task_type": t, "length": length, "difficulty": difficulty}
