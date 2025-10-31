# 🧠 ModelMatch — The AI That Chooses the Right AI

**Hackathon Submission:** You.com Hackathon 2025  
**Built by:** Adam Eccles  
**Tech Stack:** FastAPI • Python • You.com Search API • HTML/JS Frontend  

---

## 🚀 Overview

Most people don’t know which AI model to use for a given task — GPT-4, Claude, Gemini, Mistral, Grok… the options are overwhelming.

**ModelMatch** solves that problem.  
It’s an **agentic AI router** that automatically decides *which model is best for each prompt* — balancing **accuracy, cost, and latency**, so you don’t have to.

---

## 🔍 How It Works

1. **Prompt Classification** → Detects task type (code, reasoning, summarization, general).  
2. **You.com Search Integration** → Fetches benchmark and evidence data for model performance.  
3. **Scoring Engine** → Ranks models using priors and live evidence.  
4. **Model Routing** → Selects the best-performing model and executes it.  
5. **Feedback Loop** → User feedback helps adjust scoring weights over time.

**Flow Diagram:**  
`Prompt → Classifier → You Search → Scoring Engine → Chosen Model → Output`

---

## ⚙️ Key Features

- 🧠 **Dynamic Model Ranking:** Evaluates models per task type in real time.  
- ⚙️ **Mode Switching:** Choose between  
  - `Balanced` → cost + accuracy  
  - `Quality-first` → ignores cost for best output  
  - `Cost-first` → prioritizes affordability  
- 💻 **FastAPI Backend:** JSON endpoints for classification and routing.  
- 🌐 **Simple Web UI:** Lightweight HTML/JS frontend for testing and demos.  
- 💰 **Efficiency Gains:** Reduces model usage costs by **up to 70%**.  

---

## 🧩 Supported Models

| Model Name | Category | Typical Use |
|-------------|-----------|--------------|
| GPT-4 Mini | Reasoning / Coding | Complex logic, structured code |
| Claude Haiku | Writing / Context | Summarization, creative writing |
| Gemini Flash | Research | Web & document summarization |
| Mistral Small | General Tasks | Fast, low-latency, low-cost |
| You-Pro | All-rounder | Balanced capability & response quality |
| xAI Grok | Reasoning / Open Source | Advanced reasoning, analytical prompts |

---

## 🧠 Example Prompts

| Task Type | Example Prompt |
|------------|----------------|
| Code | “Write Python unit tests for a FastAPI endpoint that returns JSON.” |
| Reasoning | “Explain step-by-step why Dijkstra’s algorithm fails with negative edge weights.” |
| Search | “Summarize the latest research on quantum computing hardware in 2025.” |
| Summarization | “Summarize this paragraph in one sentence.” |
| General | “Explain the pros and cons of remote vs in-office work.” |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---------|-----------|-------------|
| `POST` | `/route` | Classifies the task, ranks models, executes the chosen model. |
| `POST` | `/feedback` | Records feedback (👍 / 👎) to improve future routing. |
| `GET` | `/metrics` | Returns live performance statistics for each model. |

---

## 🧰 Installation & Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/ModelMatch.git
cd ModelMatch

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate   # on Windows
# source .venv/bin/activate   # on macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Set API key
set YDC_API_KEY=your_youcom_api_key_here

# Run the app
uvicorn app:app --reload
