from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Enal AI OS"
    VERSION: str = "1.0.0-dev"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/enal_ai_os"
    REDIS_URL: str = "redis://localhost:6379/0"
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""

    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://localhost:11434"

    DEFAULT_MODEL: str = "gpt-4o"
    DEFAULT_REASONING_MODEL: str = "claude-3-5-sonnet-20240620"
    DEFAULT_EMBEDDING_MODEL: str = "text-embedding-3-small"

    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.7

    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "enal-ai-os"

    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_HOST: str = "http://localhost:3000"

settings = Settings()
