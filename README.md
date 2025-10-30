ModelMatch is an agentic AI router that intelligently selects the most suitable large language model (LLM) for each user prompt, optimizing for cost, latency, and task success rate.

The problem it solves is that most AI applications rely on a single model, even though tasks like reasoning, code generation, and summarization perform best on different systems. This wastes compute, increases costs, and degrades quality.

ModelMatch belongs to Track 3: Open Agentic Innovation, as it builds an autonomous, explainable system that governs other models — a meta-layer of AI coordination.

The stack includes FastAPI, Python 3.11, You.com Search (YDC Index API) for evidence retrieval, and a lightweight HTML + JavaScript web UI for testing and feedback. All routing decisions, latency, and feedback data are persisted locally and visualized in real time.

Each request to /route classifies the task type, queries You Search for benchmark context, ranks models (GPT-4 mini, Claude Haiku, Gemini Flash, Mistral Small, xAI Grok, You-Pro) using multi-factor scoring, and executes the top candidate. A /feedback endpoint logs human evaluations, continuously improving routing accuracy.

By dynamically orchestrating models, ModelMatch reduces costs by up to 70%, lowers latency, and demonstrates the future of self-optimizing AI systems that reason about which AI to trust.
