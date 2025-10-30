import os
from dotenv import load_dotenv
load_dotenv()

YDC_API_KEY = os.getenv("YDC_API_KEY", "ydc-sk-4dda9478c4ed2e71-CHWWunaejzbHqmF9auLMBsY8EZYm8U0J-448e20b1<__>1SLOAlETU8N2v5f4O6V0dB7V")

ALPHA = float(os.getenv("ROUTING_ALPHA", "0.55"))
BETA  = float(os.getenv("ROUTING_BETA",  "0.20"))
GAMMA = float(os.getenv("ROUTING_GAMMA", "0.15"))
DELTA = float(os.getenv("ROUTING_DELTA", "0.10"))


print("Loaded YDC_API_KEY:", YDC_API_KEY[:8] + "..." if YDC_API_KEY else "NOT FOUND")

