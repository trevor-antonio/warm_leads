"""
Centralized app configuration, loaded from environment variables (see .env.example).
Using pydantic-settings means every value is typed and validated at startup,
so a missing/malformed env var fails fast instead of surfacing as a weird bug later.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Server-side only — never sent to the frontend. Left blank until the LLM
    # integration step; not read anywhere yet.
    anthropic_api_key: str = ""

    # Model string is TBD — this is just the named slot to configure it later.
    anthropic_model: str = ""

    # Vite's default dev server origin, used for CORS once the frontend calls the API.
    frontend_origin: str = "http://localhost:5173"

    # SQLite file, relative to backend/ when run via uvicorn from that directory.
    # Gitignored (backend/*.db) since lead data is PII.
    database_url: str = "sqlite:///./leads.db"


settings = Settings()
