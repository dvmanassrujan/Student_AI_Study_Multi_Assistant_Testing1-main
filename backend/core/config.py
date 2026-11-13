import os
from pathlib import Path

# Safe loading of .env without hard dependency on python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    env_file = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))

class Settings:
    # Local Ollama & Hybrid Intelligence Configuration
    MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER", "ollama")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "deepseek-coder:1.3b")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "deepseek-coder:1.3b")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.3"))
    LLM_TOP_P: float = float(os.getenv("LLM_TOP_P", "0.9"))
    LLM_REPEAT_PENALTY: float = float(os.getenv("LLM_REPEAT_PENALTY", "1.1"))
    LLM_NUM_CTX: int = int(os.getenv("LLM_NUM_CTX", "8192"))
    LLM_SEED: int = int(os.getenv("LLM_SEED", "42"))
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "60"))

    # GenAI Video Intelligence Studio Settings
    YOUTUBE_API_KEY: str = os.getenv("YOUTUBE_API_KEY", "")
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "500"))
    MAX_VIDEO_DURATION_MINUTES: int = int(os.getenv("MAX_VIDEO_DURATION_MINUTES", "120"))
    MAX_CONCURRENT_JOBS: int = int(os.getenv("MAX_CONCURRENT_JOBS", "1"))
    DEFAULT_OUTPUT_LANGUAGE: str = os.getenv("DEFAULT_OUTPUT_LANGUAGE", "en")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

settings = Settings()

# Direct module-level accessors
MODEL_PROVIDER = settings.MODEL_PROVIDER
MODEL_NAME = settings.MODEL_NAME
OLLAMA_BASE_URL = settings.OLLAMA_BASE_URL
OLLAMA_MODEL = settings.OLLAMA_MODEL
MAX_UPLOAD_SIZE_MB = settings.MAX_UPLOAD_SIZE_MB
MAX_VIDEO_DURATION_MINUTES = settings.MAX_VIDEO_DURATION_MINUTES
MAX_CONCURRENT_JOBS = settings.MAX_CONCURRENT_JOBS
DEFAULT_OUTPUT_LANGUAGE = settings.DEFAULT_OUTPUT_LANGUAGE
