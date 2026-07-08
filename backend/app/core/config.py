"""Application configuration using Pydantic Settings."""
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    secret_key: str = Field("changeme", validation_alias="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    database_url: str = f"sqlite+aiosqlite:///{DATA_DIR / 'cyphermind.db'}"

    chromadb_host: str = "localhost"
    chromadb_port: int = 8001

    # NVIDIA NIM / integrate API
    nvidia_api_key: str = Field("", validation_alias="NVIDIA_API_KEY")
    nvidia_api_base: str = Field(
        "https://integrate.api.nvidia.com/v1",
        validation_alias="NVIDIA_API_BASE",
    )
    llm_model: str = Field("moonshotai/kimi-k2.6", validation_alias="LLM_MODEL")
    llm_timeout_seconds: int = Field(180, validation_alias="LLM_TIMEOUT_SECONDS")

    # Web search (Google CSE optional; DuckDuckGo fallback)
    google_api_key: str = Field("", validation_alias="GOOGLE_API_KEY")
    google_cse_id: str = Field("", validation_alias="GOOGLE_CSE_ID")

    # Bug bounty agent limits
    bug_bounty_max_iterations: int = Field(15, validation_alias="BUG_BOUNTY_MAX_ITERATIONS")

    # Local embeddings (sentence-transformers — not via NVIDIA)
    embedding_model: str = "all-MiniLM-L6-v2"

    rl_alpha: float = 0.1
    rl_gamma: float = 0.9
    rl_epsilon_start: float = 0.3
    rl_epsilon_end: float = 0.05
    rl_epsilon_decay: int = 100

    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()
