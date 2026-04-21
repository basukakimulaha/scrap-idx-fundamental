import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

FLASK_DEBUG = os.getenv("FLASK_DEBUG", "false").lower() == "true"
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

IDX_BASE_URL = "https://www.idx.co.id"
IDX_API_URL = f"{IDX_BASE_URL}/api/FundamentalAnalysis"

REQUEST_TIMEOUT = 30
