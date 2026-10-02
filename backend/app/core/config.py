from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    PROJECT_NAME: str = "Enal AI OS"
    VERSION: str = "1.0.0-dev"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = ""
    REDIS_URL: str = "redis://localhost:6379/0"
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_API_KEY: str = ""

    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = ""
    MINIO_SECRET_KEY: str = ""
    MINIO_BUCKET: str = "enal"
    MINIO_SECURE: bool = False

    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LM_STUDIO_BASE_URL: str = "http://localhost:1234/v1"
    LM_STUDIO_API_KEY: str = "lm-studio"

    DEFAULT_MODEL: str = "lmstudio/qwen/qwen3.5-9b"
    DEFAULT_REASONING_MODEL: str = "lmstudio/qwen/qwen3.5-9b"
    DEFAULT_EMBEDDING_MODEL: str = "lmstudio/text-embedding-nomic-embed-text-v1.5"

    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.7

    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    TESTING: bool = False

    LANGCHAIN_TRACING_V2: bool = False
    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "enal-ai-os"

    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_HOST: str = "http://localhost:3000"

    @model_validator(mode="after")
    def validate_secret_key(self):
        if not self.SECRET_KEY:
            raise ValueError(
                "SECRET_KEY is required. Set it via environment variable or .env file."
            )
        return self

    def require_database_url(self) -> str:
        if not self.DATABASE_URL:
            raise ValueError(
                "DATABASE_URL is required. Set it via environment variable or .env file."
            )
        return self.DATABASE_URL


settings = Settings()
